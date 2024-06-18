from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas import ContactCreate, Contact, User  # Importing schemas for type hinting
from app.db.database import get_db  # Importing the get_db function for database session
from app.repository import contacts  # Importing repository functions for CRUD operations
from app.core.auth import auth_service  # Importing authentication service (assuming this verifies current_user)

router = APIRouter()

@router.post("/contacts/", response_model=Contact)
def create_contact(
    contact: ContactCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)  # Ensure user is authorized
):
    return contacts.create_contact(db=db, contact=contact, user=current_user)

@router.get("/contacts/", response_model=List[Contact])
def read_contacts(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)  # Ensure user is authorized
):
    return contacts.get_contacts(db=db, user=current_user, skip=skip, limit=limit)

@router.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)  # Ensure user is authorized
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
    current_user: User = Depends(auth_service.get_current_user)  # Ensure user is authorized
):
    db_contact = contacts.update_contact(db=db, contact_id=contact_id, contact=contact, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/contacts/{contact_id}", response_model=Contact)
def delete_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)  # Ensure user is authorized
):
    db_contact = contacts.delete_contact(db=db, contact_id=contact_id, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
