from fastapi import APIRouter
from pydantic import BaseModel

from backend.auth.auth_handler import login

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login_user(credentials: LoginRequest):
    return login(credentials.username, credentials.password)
