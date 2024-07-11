from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Security, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import UserModel, UserResponse, TokenModel
from app.repository import users as repository_users
from app.core.auth import auth_service
from app.core.email import send_email, EmailSchema
from app.core.cloudinary import cloudinary
from app.db.models import User  # Import User model
from app.core.auth import auth_service
from app.repository.users import get_user_by_email
from app.schemas import TokenModel

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(body: UserModel, db: Session = Depends(get_db)):
    """
    Register a new user.

    Checks if the user already exists. If not, creates a new user, generates an access token,
    and sends a verification email.

    :param body: User information to register.
    :type body: UserModel
    :param db: Database session.
    :type db: Session
    :return: Newly created user information.
    :rtype: dict
    """
    exist_user = repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    
    new_user = repository_users.create_user(body, db)
    token = auth_service.create_access_token(data={"sub": body.email})
    email_schema = EmailSchema(email=body.email)
    send_email(email=email_schema, token=token)
    
    return {"user": new_user, "detail": "User successfully created. Please check your email to verify your account."}

@router.post("/login", response_model=TokenModel)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user credentials and provide an access token.

    :param form_data: Form data containing username and password.
    :type form_data: OAuth2PasswordRequestForm
    :param db: Database session.
    :type db: Session
    :return: Access token information.
    :rtype: dict
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/refresh_token', response_model=TokenModel)
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    Refresh the access token using a refresh token.

    :param credentials: HTTP Authorization credentials containing the refresh token.
    :type credentials: HTTPAuthorizationCredentials
    :param db: Database session.
    :type db: Session
    :return: New access and refresh tokens.
    :rtype: dict
    """
    token = credentials.credentials
    email = auth_service.decode_refresh_token(token)
    user = repository_users.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.refresh_token != token:
        repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = auth_service.create_access_token(data={"sub": email})
    refresh_token = auth_service.create_refresh_token(data={"sub": email})
    repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/upload-avatar", response_model=UserResponse)
def upload_avatar(file: UploadFile = File(...), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Upload and update user avatar.

    :param file: Uploaded file containing the avatar image.
    :type file: UploadFile
    :param current_user: Current authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: Session
    :return: Updated user information.
    :rtype: dict
    """
    result = cloudinary.uploader.upload(file.file)
    user = repository_users.get_user_by_email(current_user.email, db)
    user.avatar_url = result["secure_url"]
    db.commit()
    return {"user": user, "detail": "Avatar updated successfully"}
