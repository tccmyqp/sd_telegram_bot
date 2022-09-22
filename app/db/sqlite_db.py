import sqlite3 as sq
from app.config import db_name

def sql_start():
    global base, cur
    base = sq.connect(db_name)
    cur = base.cursor()
    if base:
        print('database connected')
    cur.execute("CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT")
    cur.execute("INSERT INTO menu VALUES (?,?,?,?)", tuple(data.values()))
    base.commit()
    base.close()
    
# def sql_add(st)