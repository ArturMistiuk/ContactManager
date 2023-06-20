from typing import List, Type

from sqlalchemy.orm import Session

from src.database.models import Contact, Date
from src.schemas import ContactModel
from src.repository.birthday_utils import is_upcoming_birthday


async def get_contacts(skip: int, limit: int, db: Session) -> list[Type[Contact]]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Type[Contact] | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name,
                      last_name=body.last_name,
                      email=body.email,
                      phone_number=body.phone_number,
                      birthday=body.birthday)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name,
        contact.last_name = body.last_name,
        contact.email = body.email,
        contact.phone_number = body.phone_number,
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contact(search_params, db) -> list[Type[Date]]:
    query = db.query(Contact)

    if search_params.get('first_name'):
        query = query.filter(Contact.first_name == search_params['first_name'])
    if search_params.get('last_name'):
        query = query.filter(Contact.last_name == search_params['last_name'])
    if search_params.get('email'):
        query = query.filter(Contact.email == search_params['email'])

    contacts = query.all()
    return contacts


async def get_upcoming_birthdays(db: Session) -> list[Type[Contact]]:
    contacts = db.query(Contact)
    # users = {contact.id: contact.birthday for contact in contacts if contact.birthday}
    birthdays_boys = is_upcoming_birthday([contact for contact in contacts if contact.birthday])
    birthday_boys_ids = [boy.id for boy in birthdays_boys]
    birthday_boys = db.query(Contact).filter(Contact.id.in_(birthday_boys_ids)).all()
    return birthday_boys
