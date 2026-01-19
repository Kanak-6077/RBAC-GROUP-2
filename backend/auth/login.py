# backend/auth/login.py
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from backend.auth.auth_handler import login

router = APIRouter()

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    result = login(form_data.username, form_data.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return result
