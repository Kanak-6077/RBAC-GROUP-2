import sqlite3

DB_NAME = "users.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            role TEXT
        )
    """)
    conn.commit()
    conn.close()
