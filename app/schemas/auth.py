# /home/sandeep/Projects/ScholarChat /app/schemas/auth.py

from pydantic import BaseModel, EmailStr, Field

from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


class RefreshRequest(BaseModel):
    refresh_token: str