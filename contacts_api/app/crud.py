from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import Contact
from app.schemas.contact import ContactCreate

def get_contact(db: Session, contact_id: int):
    result = db.execute(select(Contact).filter(Contact.id == contact_id))
    return result.scalars().first()

def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    result = db.execute(select(Contact).offset(skip).limit(limit))
    return result.scalars().all()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactCreate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
