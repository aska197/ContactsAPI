from pydantic import BaseModel
from typing import Optional
from datetime import date

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_info: Optional[str] = None

class Contact(ContactCreate):
    id: int

    class Config:
        orm_mode = True
