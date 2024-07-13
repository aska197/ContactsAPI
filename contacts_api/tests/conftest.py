import pytest
from starlette.testclient import TestClient
from sqlalchemy.orm import Session
from app.db import models
import sys
import os

# Ensure that the 'app' module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

print("System path after setting:", sys.path)  # Debugging print

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db import database, models

# Define the test database URL and create the engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a sessionmaker for the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[database.get_db] = override_get_db

# Create the tables in the test database
models.Base.metadata.create_all(bind=engine)

# Define the db fixture
@pytest.fixture(scope="module")
def db():
    session = TestingSessionLocal()
    yield session
    session.close()
    models.Base.metadata.drop_all(bind=engine)

# Define the client fixture
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
