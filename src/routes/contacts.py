from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactRequest, ContactResponse
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    return contact


@router.post('/', response_model=ContactResponse)
async def create_contact(body: ContactRequest, db: Session = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactRequest, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    return contact


@router.delete('/{contact_id}', response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    return contact


@router.get('/search', response_model=List[ContactResponse])
async def search_contacts(
        body: str = Query(..., description='Search contacts for name, last name or email'),
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    contacts = await repository_contacts.search_contacts(body, skip, limit, db)
    return contacts


@router.get('/birthdays/', response_model=List[ContactResponse])
async def upcoming_birthdays(db: Session = Depends(get_db)):
    upcoming_birthdays_this_year = await repository_contacts.upcoming_birthdays(db)
    return upcoming_birthdays_this_year
