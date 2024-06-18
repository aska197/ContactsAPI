from sqlalchemy.orm import Session
from app.db.models import Contact  # Import the Contact model from app.db.models
from app.schemas import ContactCreate, User  # Import the ContactCreate schema and User schema from app.schemas

def get_contact(db: Session, contact_id: int, user: User):
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()

def get_contacts(db: Session, user: User, skip: int = 0, limit: int = 10):
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate, user: User):
    db_contact = Contact(**contact.dict(), user_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactCreate, user: User):
    db_contact = get_contact(db, contact_id, user)
    if db_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, user: User):
    db_contact = get_contact(db, contact_id, user)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
