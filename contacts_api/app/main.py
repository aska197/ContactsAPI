from fastapi import FastAPI, Query
from app.db.database import engine
from app.db.session import get_db
from app.db.base import Base
from app.db.models import Contact
from app.api import contacts
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta, date
from sqlalchemy import extract

app = FastAPI()

# Include your contacts router in the app
app.include_router(contacts.router)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/")
def welcome():
    return {"message": "Welcome to my FastAPI Contacts application!"}

@app.get("/contacts/search/")
def search_contacts(
    name: str = Query(None),
    surname: str = Query(None),
    email: str = Query(None)
):
    # Create a session
    with SessionLocal() as db:
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
            query = db.query(Contact).filter(*filters)
        else:
            query = db.query(Contact)

        contacts = query.all()

    return contacts

# Define upcoming_birthdays endpoint
@app.get("/contacts/birthdays/")
def upcoming_birthdays():
    # Calculate dates for the next 7 days
    start_date = date.today()
    end_date = start_date + timedelta(days=7)

    # Extract month and day from start and end dates
    start_month = start_date.month
    start_day = start_date.day
    end_month = end_date.month
    end_day = end_date.day

    # Create a session
    with SessionLocal() as db:
        # Query contacts whose birthday month and day fall within the next 7 days
        query = db.query(Contact).filter(
            (
                (extract('month', Contact.birthday) == start_month) & (extract('day', Contact.birthday) >= start_day)
            ) |
            (
                (extract('month', Contact.birthday) == end_month) & (extract('day', Contact.birthday) <= end_day)
            )
        )
        contacts = query.all()

    return contacts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
