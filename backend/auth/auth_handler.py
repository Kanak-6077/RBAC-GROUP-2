import sqlite3
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT config
SECRET_KEY = "CHANGE_THIS_SECRET_KEY"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def authenticate_user(username: str, password: str) -> dict | None:
    conn = sqlite3.connect("users.db")
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

    return {
        "username": db_username,
        "role": role,
        "department": department
    }


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
        "access_token": create_access_token(token_payload)
    }
