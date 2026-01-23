import sqlite3
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from backend.database import get_connection 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "ce3mc4ejwrn4vi534932c42394"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(password, hashed_password)
    except Exception:
        return False 

def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str) -> dict | None:
    conn = get_connection() 
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, password, role, department FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    db_username, db_password, role, department = row
    if not verify_password(password, db_password):
        return None
    return {"username": db_username, "role": role, "department": department}

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def login(username: str, password: str) -> dict | None:
    user = authenticate_user(username, password)
    if not user:
        return None
    token_payload = {
        "sub": user["username"],
        "role": user["role"],
        "department": user["department"]
    }
    return {
        "access_token": create_access_token(token_payload),
        "token_type": "bearer",
        "user": user
    }