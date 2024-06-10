from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.contact import ContactCreate, Contact
from app import crud, schemas
from app.db.session import get_db

router = APIRouter()

@router.post("/contacts/", response_model=Contact)  # Change response_model to Contact
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_contact(db=db, contact=contact)

@router.get("/contacts/", response_model=List[Contact])
async def read_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_contacts(db, skip=skip, limit=limit)

@router.get("/contacts/{contact_id}", response_model=Contact)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/contacts/{contact_id}", response_model=Contact)
async def update_contact(contact_id: int, contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/contacts/{contact_id}", response_model=Contact)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
