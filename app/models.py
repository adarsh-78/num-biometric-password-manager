import sqlite3

def get_db_connection():
    conn = sqlite3.connect('passwords.db')
    conn.row_factory = sqlite3.Row  # So you can access columns by name
    return conn
