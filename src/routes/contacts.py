from typing import List, Dict

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse, date
from src.repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get('/upcoming-birthdays', response_model=List[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays(db)
    return contacts


@router.get("/search", response_model=List[ContactResponse])
async def search_contact(
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    db: Session = Depends(get_db),
):
    search_params = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }

    if not search_params:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='At least one parameter is required'
        )

    contact = await repository_contacts.search_contact(search_params, db)
    return contact


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel, contact_id: int, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
