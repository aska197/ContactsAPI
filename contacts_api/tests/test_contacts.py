import pytest
from fastapi import status
from app.db.models import User
from starlette.testclient import TestClient
from app.repository import users as repository_users
from app.core.auth import auth_service
from sqlalchemy.orm import Session

@pytest.mark.usefixtures("db")
class TestContactEndpoints:

    def test_create_contact(self, client: TestClient, db: Session):
        # Test creating a contact
        user = repository_users.create_user(db, username="testuser", email="test@example.com", password="password")
        login_response = client.post("/auth/login", data={"username": "testuser", "password": "password"})
        access_token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        contact_data = {"name": "John Doe", "email": "john.doe@example.com"}

        response = client.post("/contacts/", json=contact_data, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == "John Doe"
        assert response.json()["email"] == "john.doe@example.com"

    def test_read_contacts(self, client: TestClient, db: Session):
        # Test reading contacts
        user = repository_users.create_user(db, username="testuser", email="test@example.com", password="password")
        login_response = client.post("/auth/login", data={"username": "testuser", "password": "password"})
        access_token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/contacts/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_read_contact(self, client: TestClient, db: Session):
        # Test reading a specific contact
        user = repository_users.create_user(db, username="testuser", email="test@example.com", password="password")
        login_response = client.post("/auth/login", data={"username": "testuser", "password": "password"})
        access_token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        response_create = client.post("/contacts/", json={"name": "Jane Doe", "email": "jane.doe@example.com"}, headers=headers)
        contact_id = response_create.json()["id"]

        response_read = client.get(f"/contacts/{contact_id}", headers=headers)
        assert response_read.status_code == status.HTTP_200_OK
        assert response_read.json()["name"] == "Jane Doe"
        assert response_read.json()["email"] == "jane.doe@example.com"

    def test_update_contact(self, client: TestClient, db: Session):
        # Test updating a contact
        user = repository_users.create_user(db, username="testuser", email="test@example.com", password="password")
        login_response = client.post("/auth/login", data={"username": "testuser", "password": "password"})
        access_token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        response_create = client.post("/contacts/", json={"name": "Jane Doe", "email": "jane.doe@example.com"}, headers=headers)
        contact_id = response_create.json()["id"]

        updated_data = {"name": "Updated Name"}
        response_update = client.put(f"/contacts/{contact_id}", json=updated_data, headers=headers)
        assert response_update.status_code == status.HTTP_200_OK
        assert response_update.json()["name"] == "Updated Name"
        assert response_update.json()["email"] == "jane.doe@example.com"  # Ensure email remains unchanged

    def test_delete_contact(self, client: TestClient, db: Session):
        # Test deleting a contact
        user = repository_users.create_user(db, username="testuser", email="test@example.com", password="password")
        login_response = client.post("/auth/login", data={"username": "testuser", "password": "password"})
        access_token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        response_create = client.post("/contacts/", json={"name": "John Doe", "email": "john.doe@example.com"}, headers=headers)
        contact_id = response_create.json()["id"]

        response_delete = client.delete(f"/contacts/{contact_id}", headers=headers)
        assert response_delete.status_code == status.HTTP_200_OK
        assert response_delete.json()["name"] == "John Doe"
        assert response_delete.json()["email"] == "john.doe@example.com"

    def test_verify_email(self, client: TestClient, db: Session):
        # Test email verification endpoint
        user = repository_users.create_user(db, username="testuser", email="test@example.com", password="password")
        token = auth_service.create_refresh_token("test@example.com")

        response = client.get(f"/verify-email?token={token}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Email verified successfully"

