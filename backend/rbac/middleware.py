import os
import jwt
from datetime import datetime
from fastapi import Request, HTTPException, status

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

LOG_DIR = "backend/logs"
LOG_FILE = os.path.join(LOG_DIR, "access.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)


if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== ACCESS LOG STARTED ===\n")

def log_access(username: str, role: str, query: str, status_msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"{timestamp} | User: {username} | Role: {role} | "
        f"Query: {query} | Status: {status_msg}\n"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

async def enforce_rbac(request: Request, action: str, dept_requested: str = None, query: str = ""):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token missing")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    role = payload.get("role")
    department = payload.get("department")

    if role == "C-Level":
        log_access(username, role, query, "ALLOWED")
        return payload

    if dept_requested and department != dept_requested:
        log_access(username, role, query, "DENIED")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    log_access(username, role, query, "ALLOWED")
    return payload
