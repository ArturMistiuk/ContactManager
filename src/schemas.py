from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date


class ContactModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    email: EmailStr = Field()
    phone_number: Optional[str] = Field(max_length=13)
    birthday: Optional[date]


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True
