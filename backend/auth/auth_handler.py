from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from backend.database import get_connection

# ✅ Use PBKDF2 instead of bcrypt (Windows-safe)
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

SECRET_KEY = "ce3mc4ejwrn4vi534932c42394"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()

    print(f"[DEBUG] Searching for user: '{username}'")
    cursor.execute(
        "SELECT username, password, role, department FROM users WHERE username = ?",
        (username,),
    )
    row = cursor.fetchone()
    print(f"[DEBUG] Database query result: {row}")
    conn.close()

    if not row:
        print(f"[DEBUG] User '{username}' not found in database")
        return None
    
    db_username, db_password, role, department = row
    print(f"[DEBUG] Found user: '{db_username}', verifying password...")

    if not verify_password(password, db_password):
        print(f"[DEBUG] Password verification failed for user '{username}'")
        return None

    return {
        "username": db_username,
        "role": role,
        "department": department,
    }


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def login(username: str, password: str) -> dict:
    user = authenticate_user(username, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "access_token": create_access_token({
            "sub": user["username"],
            "role": user["role"],
            "department": user["department"],
        }),
        "token_type": "bearer",
    }
