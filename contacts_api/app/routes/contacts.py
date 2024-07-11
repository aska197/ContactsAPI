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
    """
    Create a new contact for the authenticated user.

    :param contact: Contact information to create.
    :type contact: ContactCreate
    :param request: HTTP request object.
    :type request: Request
    :param db: Database session.
    :type db: Session
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: Newly created contact information.
    :rtype: Contact
    """
    return contacts.create_contact(db=db, contact=contact, user=current_user)

@router.get("/contacts/", response_model=List[Contact])
def read_contacts(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    Retrieve contacts for the authenticated user with optional pagination.

    :param skip: Number of contacts to skip.
    :type skip: int
    :param limit: Maximum number of contacts to return.
    :type limit: int
    :param db: Database session.
    :type db: Session
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: List of contacts.
    :rtype: List[Contact]
    """
    return contacts.get_contacts(db=db, user=current_user, skip=skip, limit=limit)

@router.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    Retrieve a specific contact by ID for the authenticated user.

    :param contact_id: ID of the contact to retrieve.
    :type contact_id: int
    :param db: Database session.
    :type db: Session
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: Contact information.
    :rtype: Contact
    """
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
    """
    Update a specific contact by ID for the authenticated user.

    :param contact_id: ID of the contact to update.
    :type contact_id: int
    :param contact: Updated contact information.
    :type contact: ContactCreate
    :param db: Database session.
    :type db: Session
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: Updated contact information.
    :rtype: Contact
    """
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
    """
    Delete a specific contact by ID for the authenticated user.

    :param contact_id: ID of the contact to delete.
    :type contact_id: int
    :param db: Database session.
    :type db: Session
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: Deleted contact information.
    :rtype: Contact
    """
    db_contact = contacts.delete_contact(db=db, contact_id=contact_id, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verify user's email using the provided token.

    :param token: Token for email verification.
    :type token: str
    :param db: Database session.
    :type db: Session
    :return: Confirmation message.
    :rtype: dict
    """
    email = auth_service.decode_refresh_token(token)
    user = repository_users.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token or user does not exist")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}