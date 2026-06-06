from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TodoCreate(BaseModel):
    title: str
    priority: int = 1  # 0=low, 1=medium, 2=high
    due_date: Optional[date] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    due_date: Optional[date] = None

class TodoResponse(BaseModel):
    id: str
    title: str
    priority: int
    status: str
    due_date: Optional[date]
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
