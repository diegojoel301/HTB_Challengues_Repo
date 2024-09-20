import { Database as sqlite } from 'sqlite-async';
import crypto from "crypto";

const md5 = data => crypto.createHash('md5').update(data).digest("hex");

export class Database {
    constructor(db_file) {
        this.db_file = db_file;
        this.db = undefined;
    }

    async connect() {
        this.db = await sqlite.open(this.db_file);
    }

    async migrate() {
        let password = md5(crypto.randomBytes(16).toString('hex'));

        return this.db.exec(`
            DROP TABLE IF EXISTS users;

            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username   VARCHAR(255) NOT NULL UNIQUE,
                password   VARCHAR(255) NOT NULL,
                verified   BOOLEAN      NOT NULL DEFAULT false
            );

            INSERT INTO users (username, password, verified) VALUES ('admin', '${password}', true);

            DROP TABLE IF EXISTS enrollments;

            CREATE TABLE IF NOT EXISTS enrollments (
                id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username   VARCHAR(255) NOT NULL UNIQUE,
                full_name VARCHAR(255) NULL,
                phone   VARCHAR(255) NULL,
                birth_date   VARCHAR(255) NULL,
                gender   VARCHAR(255) NULL,
                biography   TEXT NULL,
                resume_file VARCHAR(256) NULL
            );

            DROP TABLE IF EXISTS settings;

            CREATE TABLE settings(
                id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                config_key          VARCHAR(2) NOT NULL,
                config_val          NUMERIC(9,6) NOT NULL
            );
            INSERT INTO settings (config_key, config_val)
            VALUES
                ('sms_verb', 'POST'),
                ('sms_url', 'https://platform.clickatell.com/messages'),
                ('sms_params', '{"apiKey" : "xxxx", "toNumber": "recipient", "text": "message"}'),
                ('sms_headers', 'Content-Type: application/json\nAuthorization: Basic YWRtaW46YWRtaW4='),
                ('sms_resp_ok', '<status>ok</status>'),
                ('sms_resp_bad', '<status>error</status>');
        `);
    }

    async registerUser(username, password) {
        return new Promise(async (resolve, reject) => {
            try {
                let register_sql = await this.db.prepare('INSERT INTO users (username, password) VALUES ( ?, ?)');
                let enrollment_sql = await this.db.prepare('INSERT INTO enrollments (username) VALUES (?)');

                await register_sql.run(username, md5(password));
                await enrollment_sql.run(username);

                resolve();
            } catch(e) {
                reject(e);
            }
        });
    }

    async loginUser(username, password) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT username FROM users WHERE username = ? and password = ?');
                resolve(await stmt.get(username, md5(password)));
            } catch(e) {
                reject(e);
            }
        });
    }

    async getUser(username) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT * FROM users WHERE username = ?');
                resolve(await stmt.get(username));
            } catch(e) {
                reject(e);
            }
        });
    }

    async checkUser(username) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT username FROM users WHERE username = ?');
                let row = await stmt.get(username);
                resolve(row !== undefined);
            } catch(e) {
                reject(e);
            }
        });
    }

    async getFormData(username) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT * FROM enrollments WHERE username = ?');
                resolve(await stmt.get(username));
            } catch(e) {
                reject(e);
            }
        });
    }

    async updateEnrollment(full_name, phone, birth_date, gender, biography, username) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare(`
                    UPDATE enrollments
                    SET
                        full_name = ?,
                        phone = ?,
                        birth_date = ?,
                        gender = ?,
                        biography = ?
                    WHERE username = ?
                `);
                resolve((await stmt.run(full_name, phone, birth_date, gender, biography, username)));
            } catch(e) {
                reject(e);
            }
        });
    }

    async setResume(filename, username) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('UPDATE enrollments SET resume_file = ? WHERE username = ?');
                resolve((await stmt.run(filename, username)));
            } catch(e) {
                reject(e);
            }
        });
    }

    async saveSMSConfig(verb, url, params, headers, resp_ok, resp_bad) {
        return new Promise(async (resolve, reject) => {
            const smsConfig = {
                'sms_verb': verb,
                'sms_url': url,
                'sms_params': params,
                'sms_headers': headers,
                'sms_resp_ok': resp_ok,
                'sms_resp_bad': resp_bad
            }
            for(const [col_name, col_data] of Object.entries(smsConfig)) {
                try {
                    let stmt = await this.db.prepare('UPDATE settings SET config_val = ? WHERE config_key = ?');
                    await stmt.run(col_data, col_name)
                } catch(e) {
                    reject(e);
                }
            }
            resolve(true);
        });
    }

}
