from typing import List, Dict

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.models import User
from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse, date
from src.repository import contacts as repository_contacts
from src.routes.auth import auth_service


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get('/upcoming-birthdays', response_model=List[ContactResponse], description='No more than 3 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_upcoming_birthdays(db: Session = Depends(get_db),  current_user: User = Depends(auth_service.get_current_user)):
    """
The get_upcoming_birthdays function returns a list of contacts with upcoming birthdays.

:param db: Session: Get the database session, which is used to query the database
:param current_user: User: Get the user id of the currently logged in user
:return: A list of contacts with upcoming birthdays
:rtype: List[Contact]
    """
    contacts = await repository_contacts.get_upcoming_birthdays(db, current_user)
    return contacts


@router.get("/search", response_model=List[ContactResponse], description='No more than 3 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contact(
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    """
The search_contact function searches for a contact in the database.

:param first_name: str: Specify the first name of the contact to be searched for
:param last_name: str: Filter the results by last name
:param email: str: Search for a contact by email
:param db: Session: Get the database session
:param current_user: User: Get the user who is logged in
:return: A list of contacts
:rtype: Contact
    """
    search_params = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }

    if not search_params:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='At least one parameter is required'
        )

    contact = await repository_contacts.search_contact(search_params, current_user, db)
    return contact


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
The read_contacts function returns a list of contacts.

:param skip: int: Skip the first n contacts
:param limit: int: Limit the number of contacts returned
:param db: Session: Access the database
:param current_user: User: Get the current user
:return: A list of contacts
:rtype: List[Contact]
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
The read_contact function is a GET request that returns the contact with the given ID.
It requires an authorization token and will return a 404 error if no contact exists with that ID.

:param contact_id: int: Specify the contact id
:param db: Session: Pass the database session to the repository layer
:param current_user: User: Get the current user from the auth_service
:return: The contact object
:rtype: List[Contact]
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, description='No more than 3 requests per minute', dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
The create_contact function creates a new contact in the database.
    The function takes a ContactModel object as input, which is validated by pydantic.
    The function also takes an optional db Session object and current_user User object as inputs,
        both of which are provided by dependency injection via FastAPI's Depends() decorator.

:param body: ContactModel: Get the data from the request body
:param db: Session: Pass the database session to the repository function
:param current_user: User: Get the user that is currently logged in
:return: Contact
:rtype: Contact
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(
    body: ContactModel, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)
):
    """
The update_contact function updates a contact in the database.
    The function takes an id of the contact to update, and a body containing the new data for that contact.
    It returns an updated ContactModel object.

:param body: ContactModel: Pass the contact data to update
:param contact_id: int: Find the contact in the database
:param db: Session: Pass the database session to the repository
:param current_user: User: Get the user from the database
:return: The Contact that was updated
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
The remove_contact function removes a contact from the database.
    It takes in an integer representing the id of the contact to be removed, and returns a Contact object.

:param contact_id: int: Specify the contact to be removed
:param db: Session: Pass the database session to the repository
:param current_user: User: Get the current user, and the db: session parameter is used to get a database session
:return: The contact that was removed
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
