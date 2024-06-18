from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=16)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=10)

class UserModel(BaseModel):
    id: int
    username: str = Field(..., min_length=5, max_length=16)
    email: EmailStr
    created_at: datetime
    avatar: Optional[str] = None

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    created_at: datetime
    avatar: Optional[str] = None

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user: User
    detail: str = "User successfully created"

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
