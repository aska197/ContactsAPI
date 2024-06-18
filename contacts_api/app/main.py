from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy import extract
from datetime import date, timedelta
from typing import List

from app.db.database import engine, Base, get_db
from app.db.models import Contact
from app.routes import contacts as contacts_router, auth as auth_router
from app.core.auth import auth_service
from app.schemas import Contact as ContactSchema, User  # Import schema for response model and User

# Create FastAPI app
app = FastAPI()

# Include routers
app.include_router(auth_router.router, prefix='/api')
app.include_router(contacts_router.router, prefix='/api')

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Root route
@app.get("/")
def welcome():
    return {"message": "Welcome to my FastAPI Contacts application!"}

# Search contacts endpoint
@app.get("/contacts/search/", response_model=List[ContactSchema])
def search_contacts(
    name: str = Query(None, description="Filter contacts by first name"),
    surname: str = Query(None, description="Filter contacts by last name"),
    email: str = Query(None, description="Filter contacts by email"),
    current_user: User = Depends(auth_service.get_current_user)  # Ensure user is authorized
):
    with SessionLocal() as db:
        filters = []
        if name:
            filters.append(Contact.first_name.ilike(f"%{name}%"))
        if surname:
            filters.append(Contact.last_name.ilike(f"%{surname}%"))
        if email:
            filters.append(Contact.email.ilike(f"%{email}%"))

        if filters:
            query = db.query(Contact).filter(*filters)
        else:
            query = db.query(Contact)

        contacts = query.all()

    return contacts

# Upcoming birthdays endpoint
@app.get("/contacts/birthdays/", response_model=List[ContactSchema])
def upcoming_birthdays(
    current_user: User = Depends(auth_service.get_current_user)  # Ensure user is authorized
):
    # Calculate dates for the next 7 days
    start_date = date.today()
    end_date = start_date + timedelta(days=7)

    # Extract month and day from start and end dates
    start_month = start_date.month
    start_day = start_date.day
    end_month = end_date.month
    end_day = end_date.day

    with SessionLocal() as db:
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

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
