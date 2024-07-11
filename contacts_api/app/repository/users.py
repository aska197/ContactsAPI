from typing import Union
from libgravatar import Gravatar
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas import UserModel
from app.core.auth import auth_service  # Assuming auth_service is used for password hashing

def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieve a user by email from the database.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: Database session.
    :type db: Session
    :return: The user corresponding to the email address.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> User:
    """
    Retrieve a user by username from the database.

    :param db: Database session.
    :type db: Session
    :param username: The username of the user to retrieve.
    :type username: str
    :return: The user corresponding to the username.
    :rtype: User
    """
    return db.query(User).filter(User.username == username).first()

def create_user(body: UserModel, db: Session) -> User:
    """
    Create a new user in the database.

    This function also attempts to fetch the user's avatar using Gravatar.

    :param body: User information to create.
    :type body: UserModel
    :param db: Database session.
    :type db: Session
    :return: The created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(f"Error fetching avatar for {body.email}: {e}")
        # Handle avatar retrieval errors as needed

    new_user = User(
        username=body.username,
        email=body.email,
        password=auth_service.get_password_hash(body.password),
        avatar=avatar
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_token(user: User, token: Union[str, None], db: Session) -> None:
    """
    Update the refresh token for a user.

    :param user: The user whose token is being updated.
    :type user: User
    :param token: The new refresh token (or None to clear the token).
    :type token: Union[str, None]
    :param db: Database session.
    :type db: Session
    :return: None
    :rtype: None
    """
    user.refresh_token = token
    db.commit()
