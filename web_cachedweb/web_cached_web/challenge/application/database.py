from flask import g
from sqlite3 import dbapi2 as sqlite3

def connect_db():
    return sqlite3.connect('cached_web.db', isolation_level=None)
    
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = [dict((cur.description[idx][0], value) \
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (next(iter(rv[0].values())) if rv else None) if one else rv