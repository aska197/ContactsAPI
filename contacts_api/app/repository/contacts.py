from sqlalchemy.orm import Session
from app.db.models import Contact  # Import the Contact model from app.db.models
from app.schemas import ContactCreate, User  # Import the ContactCreate schema and User schema from app.schemas

def get_contact(db: Session, contact_id: int, user: User):
    """
    Retrieve a specific contact belonging to the authenticated user.

    :param db: Database session.
    :type db: Session
    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The authenticated user.
    :type user: User
    :return: The contact matching the contact_id and belonging to the user.
    :rtype: Contact
    """
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()

def get_contacts(db: Session, user: User, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of contacts belonging to the authenticated user with pagination.

    :param db: Database session.
    :type db: Session
    :param user: The authenticated user.
    :type user: User
    :param skip: Number of contacts to skip.
    :type skip: int, optional
    :param limit: Maximum number of contacts to return.
    :type limit: int, optional
    :return: A list of contacts belonging to the user.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate, user: User):
    """
    Create a new contact for the authenticated user.

    :param db: Database session.
    :type db: Session
    :param contact: Contact information to create.
    :type contact: ContactCreate
    :param user: The authenticated user.
    :type user: User
    :return: The created contact.
    :rtype: Contact
    """
    db_contact = Contact(**contact.dict(), user_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactCreate, user: User):
    """
    Update an existing contact belonging to the authenticated user.

    :param db: Database session.
    :type db: Session
    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param contact: Updated contact information.
    :type contact: ContactCreate
    :param user: The authenticated user.
    :type user: User
    :return: The updated contact.
    :rtype: Contact
    """
    db_contact = get_contact(db, contact_id, user)
    if db_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, user: User):
    """
    Delete a specific contact belonging to the authenticated user.

    :param db: Database session.
    :type db: Session
    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :param user: The authenticated user.
    :type user: User
    :return: The deleted contact.
    :rtype: Contact
    """
    db_contact = get_contact(db, contact_id, user)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
