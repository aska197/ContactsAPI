from typing import Union
from libgravatar import Gravatar
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas import UserModel
from app.core.auth import auth_service  # Assuming auth_service is used for password hashing

def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def create_user(body: UserModel, db: Session) -> User:
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
    user.refresh_token = token
    db.commit()
