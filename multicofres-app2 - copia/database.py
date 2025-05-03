import pymysql
from flask import g

# Configuración de conexión a la base de datos
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="15Octubre2005$",
        database="multicofresdb",
        cursorclass=pymysql.cursors.DictCursor
    )

def get_db():
    if 'db' not in g:
        g.db = connect_db()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
