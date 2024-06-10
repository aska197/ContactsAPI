from fastapi import FastAPI, Query
from app.db.database import engine
from app.db.session import get_db
from app.db.base import Base
from app.db.models import Contact
from app.api import contacts
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, date
from sqlalchemy import select



app = FastAPI()

# Include your contacts router in the app
app.include_router(contacts.router)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/")
async def welcome():
    return {"message": "Welcome to my FastAPI Contacts application!"}

@app.on_event("startup")
async def startup_event():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/contacts/search/")
async def search_contacts(
    name: str = Query(None),
    surname: str = Query(None),
    email: str = Query(None)
):
    # Create a session
    async with get_db() as db:
        # Define filters based on query parameters
        filters = []
        if name:
            filters.append(Contact.first_name.ilike(f"%{name}%"))
        if surname:
            filters.append(Contact.last_name.ilike(f"%{surname}%"))
        if email:
            filters.append(Contact.email.ilike(f"%{email}%"))

        # Execute the query
        if filters:
            query = db.execute(select(Contact).filter(*filters))
            contacts = await query.scalars().all()
        else:
            query = db.execute(select(Contact))
            contacts = await query.scalars().all()

    return contacts

# Define upcoming_birthdays endpoint
@app.get("/contacts/birthdays/")
async def upcoming_birthdays():
    # Calculate dates for the next 7 days
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=7)

    # Create a session
    async with get_db() as db:
        # Execute the query to select contacts with birthdays in this range
        query = select(Contact).filter(Contact.birthday >= start_date, Contact.birthday < end_date)
        result = await db.execute(query)
        contacts = await result.scalars().all()

    return contacts


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
