from typing import Type
from sqlalchemy.orm import Session
from libgravatar import Gravatar
from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> Type[User] | None:
    """
The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists, it returns None.

:param email: str: Pass in the email of the user that we want to get from our database
:param db: Session: Pass the database session into the function
:return: The user object if the user exists, or none if it doesn't
:rtype: User | None
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
The create_user function creates a new user in the database.

:param body: UserModel: Get the user data from the request body
:param db: Session: Access the database
:return: A user object
:rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: Type[User], token: str | None, db: Session) -> None:
    """
The update_token function updates the refresh token for a user.
    Args:
        user (User): The User object to update.
        token (str | None): The new refresh token to set for the user. If None, then no change is made and an error is logged instead.
        db (Session): A database session that can be used to commit changes.

:param user: Type[User]: Specify the type of object that is passed to the function
:param token: str | None: Update the refresh token in the database
:param db: Session: Pass the database session to the function
:return: None
:rtype: None type
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


:param email: str: Get the email of the user
:param db: Session: Pass the database session to the function
:return: None
:rtype: None type
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
The update_avatar function updates the avatar of a user.

:param email: Get the user from the database
:param url: str: Specify the type of data that is being passed to the function
:param db: Session: Pass the database session to the function
:return: The updated user
:rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
