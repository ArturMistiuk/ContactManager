from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, Date, User
from src.schemas import ContactModel
from src.repository.birthday_utils import is_upcoming_birthday


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> list[Type[Contact]]:
    """
The get_contacts function returns a list of contacts for the user.

:param skip: int: Skip the first n contacts
:param limit: int: Limit the number of contacts returned
:param user: User: Get the contacts for a specific user
:param db: Session: Access the database
:return: A list of contact objects
:rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Type[Contact] | None:
    """
The get_contact function takes in a contact_id and user, and returns the Contact object with that id.
    If no such contact exists, it returns None.

:param contact_id: int: Specify the id of the contact to be retrieved
:param user: User: Get the user from the database
:param db: Session: Pass the database session to the function
:return: A contact object from the database
:rtype: List[Note]
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:

    """
The create_contact function creates a new contact in the database.

:param body: ContactModel: Get the data from the request body
:param user: User: Get the user_id from the user object
:param db: Session: Access the database
:return: A contact object
:rtype: Contact
    """
    contact = Contact(first_name=body.first_name,
                      last_name=body.last_name,
                      email=body.email,
                      phone_number=body.phone_number,
                      birthday=body.birthday,
                      user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
The update_contact function updates a contact in the database.
    Args:
        contact_id (int): The id of the contact to update.
        body (ContactModel): The updated ContactModel object with new values for first_name, last_name, email, phone_number and birthday.
        user (User): The User object that is currently logged in and making this request. This is used to ensure that only contacts belonging to this user are updated by themselfs or an admin/superuser.

:param contact_id: int: Identify the contact to be updated
:param body: ContactModel: Pass in the contact information to be updated
:param user: User: Get the user id of the logged in user
:param db: Session: Access the database
:return: The updated contact object
:rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name,
        contact.last_name = body.last_name,
        contact.email = body.email,
        contact.phone_number = body.phone_number,
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
The remove_contact function removes a contact from the database.
    Args:
        contact_id (int): The id of the contact to be removed.
        user (User): The user who owns the contacts list.
        db (Session): A connection to our database, used for querying and deleting data.

:param contact_id: int: Identify the contact to be removed
:param user: User: Identify the user who is making the request
:param db: Session: Access the database
:return: A contact object if the contact was successfully removed from the database
:rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contact(search_params, user: User, db) -> list[Type[Date]]:
    """
The search_contact function searches for contacts in the database.
    Args:
        search_params (dict): A dictionary of parameters to filter by.
        user (User): The user who is searching for contacts.

:param search_params: Filter the contacts based on the parameters passed in
:param user: User: Get the user id from the database
:param db: Pass the database connection to the function
:return: A list of contact objects
:rtype: List[Contact]
    """
    query = db.query(Contact).filter(Contact.user_id == user.id)

    if search_params.get('first_name'):
        query = query.filter(Contact.first_name == search_params['first_name'])
    if search_params.get('last_name'):
        query = query.filter(Contact.last_name == search_params['last_name'])
    if search_params.get('email'):
        query = query.filter(Contact.email == search_params['email'])

    contacts = query.all()
    return contacts


async def get_upcoming_birthdays(db: Session, user: User) -> list[Type[Contact]]:
    """
The get_upcoming_birthdays function returns a list of contacts whose birthday is upcoming.
    Args:
        db (Session): The database session to use for querying the data.
        user (User): The user who's contacts are being searched through.

:param db: Session: Pass the database session to the function
:param user: User: Get the user's id from the database
:return: A list of contact objects
:rtype: List[Contact]
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id)
    birthdays_boys = is_upcoming_birthday([contact for contact in contacts if contact.birthday])
    birthday_boys_ids = [boy.id for boy in birthdays_boys]
    birthday_boys = db.query(Contact).filter(Contact.id.in_(birthday_boys_ids)).all()
    return birthday_boys
