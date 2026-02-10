import sqlite3
import os

# Use absolute path to frontend/users.db for shared database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "frontend", "users.db")

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            department TEXT
        )
    """)
    conn.commit()
    conn.close()
