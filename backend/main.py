from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="RBAC Backend - Milestone 3 Task 1")

# ---------- DATABASE SETUP ----------
def get_connection():
    return sqlite3.connect("users.db")

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

create_user_table()

# ---------- DATA MODEL ----------
class User(BaseModel):
    username: str
    role: str

# ---------- API ENDPOINTS ----------
@app.get("/")
def root():
    return {"message": "Backend running successfully"}

@app.post("/users")
def create_user(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, role) VALUES (?, ?)",
        (user.username, user.role)
    )
    conn.commit()
    conn.close()
    return {"status": "User created"}

@app.get("/users")
def list_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users
