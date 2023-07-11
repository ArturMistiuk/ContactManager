from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date


class ContactModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    email: EmailStr
    phone_number: Optional[str] = Field(max_length=13)
    birthday: Optional[date]


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)


class UserDb(BaseModel):
    id: int    # Optional[int]
    # first_name: str
    # last_name: str
    username: str
    email: EmailStr
    password: str
    avatar: str
    # refresh_token: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = 'User successfully created'


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RequestEmail(BaseModel):
    email: EmailStr
