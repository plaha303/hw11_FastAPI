from datetime import date

from pydantic import BaseModel


class ContactRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
