from pydantic import BaseModel, validator

class User(BaseModel):
    username: str
    password: str
    role: str
    department: str

    @validator("password")
    def password_length_check(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long for bcrypt encryption")
        return v
