from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

# Fake token store (for Task 1 only)
FAKE_TOKENS = {
    "admin-token": "Admin",
    "employee-token": "Employee",
    "manager-token": "Manager"
}

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    if token not in FAKE_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )

    return {
        "role": FAKE_TOKENS[token],
        "token": token
    }
