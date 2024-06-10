from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Contact
from app.schemas.contact import ContactCreate

async def get_contact(db: AsyncSession, contact_id: int):
    result = await db.execute(select(Contact).filter(Contact.id == contact_id))
    return result.scalars().first()

async def get_contacts(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Contact).offset(skip).limit(limit))
    return result.scalars().all()

async def create_contact(db: AsyncSession, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

async def update_contact(db: AsyncSession, contact_id: int, contact: ContactCreate):
    db_contact = await get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        await db.commit()
        await db.refresh(db_contact)
    return db_contact

async def delete_contact(db: AsyncSession, contact_id: int):
    db_contact = await get_contact(db, contact_id)
    if db_contact:
        await db.delete(db_contact)
        await db.commit()
    return db_contact
