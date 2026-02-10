import sqlite3
from pathlib import Path
import os
import bcrypt

# Use same database as backend: frontend/users.db
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "frontend" / "users.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT,
            department TEXT
        )
        """)


def create_user(username, password, role, department):
    init_db()

    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO users (username, password, role, department) VALUES (?, ?, ?, ?)",
                (username, password_hash, role, department)
            )
        return True, None
    except sqlite3.IntegrityError:
        return False, "Username already exists"


def get_all_users():
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT username, role, department FROM users ORDER BY username"
        ).fetchall()

    return [
        {"username": r[0], "role": r[1], "department": r[2]}
        for r in rows
    ]


def delete_user(username):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM users WHERE username = ?",
            (username,)
        )
