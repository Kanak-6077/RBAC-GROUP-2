import sqlite3
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from backend.database import get_connection 

# 1. Setup Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. JWT Configuration
SECRET_KEY = "CHANGE_THIS_TO_A_SECURE_RANDOM_STRING"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Hashes a plain-text password."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a stored hash."""
    try:
        return pwd_context.verify(password, hashed_password)
    except Exception:
        # Prevents crash if the database accidentally contains plain text
        return False 

def create_access_token(data: dict) -> str:
    """Generates a JWT access token."""
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str) -> dict | None:
    """Checks credentials against the database and returns user data."""
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
    
    # Check if the typed password matches the hash in the DB
    if not verify_password(password, db_password):
        return None

    return {"username": db_username, "role": role, "department": department}

# 3. THIS IS THE FUNCTION YOUR LOGIN.PY IS LOOKING FOR
def login(username: str, password: str) -> dict | None:
    """Main login logic used by the API router."""
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
        "token_type": "bearer"
    }