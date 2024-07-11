import pytest
from starlette.testclient import TestClient
import sys
import os

# Insert the parent directory of the project into sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import your FastAPI app
from app.main import app

# If needed, import database session and engine
from app.db.database import SessionLocal, engine

# Create fixtures or setup functions as needed
@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c



