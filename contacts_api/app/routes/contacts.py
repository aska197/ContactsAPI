from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas import ContactCreate, Contact, User
from app.db.database import get_db
from app.repository import contacts, users as repository_users
from app.core.auth import auth_service

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/contacts/", response_model=Contact)
@limiter.limit("5/minute")
def create_contact(
    contact: ContactCreate, 
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    return contacts.create_contact(db=db, contact=contact, user=current_user)

@router.get("/contacts/", response_model=List[Contact])
def read_contacts(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    return contacts.get_contacts(db=db, user=current_user, skip=skip, limit=limit)

@router.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    db_contact = contacts.get_contact(db=db, contact_id=contact_id, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int, 
    contact: ContactCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    db_contact = contacts.update_contact(db=db, contact_id=contact_id, contact=contact, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/contacts/{contact_id}", response_model=Contact)
def delete_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    db_contact = contacts.delete_contact(db=db, contact_id=contact_id, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = auth_service.decode_refresh_token(token)
    user = repository_users.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token or user does not exist")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}