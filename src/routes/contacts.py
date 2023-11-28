from typing import List
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact, ContactRequest, ContactResponse


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return contact


@router.post('/', response_model=ContactResponse)
async def create_contact(body: ContactRequest, db: Session = Depends(get_db)):
    db_contact = Contact(**body.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactRequest, contact_id: int, db: Session = Depends(get_db)):
    contact =  db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')

    for attr, value in body.model_dump().items():
        setattr(contact, attr, value)

    db.commit()
    db.refresh(contact)
    return contact


@router.delete('/{contact_id}', response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    db.delete(contact)
    db.commit()
    return contact


@router.get('/', response_model=List[ContactResponse])
async def search_contacts(
        body: str = Query(..., description='Search contacts for name, last name or email'),
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    contacts = db.query(Contact).filter(
        Contact.first_name.ilike(f'%{body}%')
        | Contact.last_name.ilike(f'%{body}%')
        | Contact.email.ilike(f'%{body}%')
    ).offset(skip).limit(limit).all()
    return contacts


@router.get('/birthdays/', response_model=List[ContactResponse])
async def upcoming_birthdays(db: Session = Depends(get_db)):
    todey = datetime.today()
    seven_days_after = todey + timedelta(days=7)

    upcoming_birthdays_this_year = db.query(Contact).filter(
        text("TO_CHAR(birthday, 'MM-DD') BETWEEN :start_date AND :end_date")
    ).params(start_date=todey.strftime('%m-%d'), end_date=seven_days_after.strftime('%m-%d')).all()
    return upcoming_birthdays_this_year
