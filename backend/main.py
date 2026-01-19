from fastapi import FastAPI
from backend.models import User
from backend.database import get_connection, create_user_table

app = FastAPI(title="RBAC Backend - Milestone 3 Task 1")

create_user_table()

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

