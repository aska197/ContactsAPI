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
    exist_user = repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    
    # Create the user without hashing the password here
    new_user = repository_users.create_user(body, db)
    
    # Generate token and send verification email
    token = auth_service.create_access_token(data={"sub": body.email})
    
    # Ensure email is passed as EmailSchema instance
    email_schema = EmailSchema(email=body.email)
    
    # Call send_email with the correct parameters
    send_email(email=email_schema, token=token)
    
    return {"user": new_user, "detail": "User successfully created. Please check your email to verify your account."}

@router.post("/login", response_model=TokenModel)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/refresh_token', response_model=TokenModel)
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
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
    result = cloudinary.uploader.upload(file.file)
    user = repository_users.get_user_by_email(current_user.email, db)
    user.avatar_url = result["secure_url"]
    db.commit()
    return {"user": user, "detail": "Avatar updated successfully"}
