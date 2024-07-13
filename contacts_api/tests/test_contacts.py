import pytest
from unittest.mock import MagicMock, patch
from app.db.models import User
from app.core.auth import auth_service
from app.schemas import ContactCreate, Contact
from app.repository import contacts, users as repository_users

@pytest.fixture()
def token(client, user, session, monkeypatch):
    # Mock any necessary services or methods
    mock_send_email = MagicMock()
    monkeypatch.setattr("app.routes.auth.send_email", mock_send_email)
    
    # Create and confirm user
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    
    # Get login token
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')}
    )
    data = response.json()
    return data["access_token"]

def test_create_contact(client, token):
    with patch.object(contacts, 'create_contact') as create_contact_mock:
        create_contact_mock.return_value = Contact(id=1, **{
            "name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "1234567890"
        })
        response = client.post(
            "/api/contacts/",
            json={"name": "John Doe", "email": "johndoe@example.com", "phone": "1234567890"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "John Doe"
        assert "id" in data

def test_read_contacts(client, token):
    with patch.object(contacts, 'get_contacts') as get_contacts_mock:
        get_contacts_mock.return_value = [
            Contact(id=1, **{"name": "John Doe", "email": "johndoe@example.com", "phone": "1234567890"})
        ]
        response = client.get(
            "/api/contacts/",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["name"] == "John Doe"
        assert "id" in data[0]

def test_read_contact(client, token):
    with patch.object(contacts, 'get_contact') as get_contact_mock:
        get_contact_mock.return_value = Contact(id=1, **{
            "name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "1234567890"
        })
        response = client.get(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "John Doe"
        assert "id" in data

def test_read_contact_not_found(client, token):
    with patch.object(contacts, 'get_contact') as get_contact_mock:
        get_contact_mock.return_value = None
        response = client.get(
            "/api/contacts/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

def test_update_contact(client, token):
    with patch.object(contacts, 'update_contact') as update_contact_mock:
        update_contact_mock.return_value = Contact(id=1, **{
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "phone": "0987654321"
        })
        response = client.put(
            "/api/contacts/1",
            json={"name": "Jane Doe", "email": "janedoe@example.com", "phone": "0987654321"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Jane Doe"
        assert "id" in data

def test_update_contact_not_found(client, token):
    with patch.object(contacts, 'update_contact') as update_contact_mock:
        update_contact_mock.return_value = None
        response = client.put(
            "/api/contacts/2",
            json={"name": "Jane Doe", "email": "janedoe@example.com", "phone": "0987654321"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

def test_delete_contact(client, token):
    with patch.object(contacts, 'delete_contact') as delete_contact_mock:
        delete_contact_mock.return_value = Contact(id=1, **{
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "phone": "0987654321"
        })
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["name"] == "Jane Doe"
        assert "id" in data

def test_delete_contact_not_found(client, token):
    with patch.object(contacts, 'delete_contact') as delete_contact_mock:
        delete_contact_mock.return_value = None
        response = client.delete(
            "/api/contacts/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"

def test_verify_email(client):
    with patch.object(auth_service, 'decode_refresh_token') as decode_token_mock:
        decode_token_mock.return_value = "testuser@example.com"
        with patch.object(repository_users, 'get_user_by_email') as get_user_mock:
            get_user_mock.return_value = User(email="testuser@example.com", is_verified=False)
            response = client.get(
                "/api/verify-email",
                params={"token": "valid_token"}
            )
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["message"] == "Email verified successfully"

def test_verify_email_invalid_token(client):
    with patch.object(auth_service, 'decode_refresh_token') as decode_token_mock:
        decode_token_mock.return_value = None
        response = client.get(
            "/api/verify-email",
            params={"token": "invalid_token"}
        )
        assert response.status_code == 400, response.text
        data = response.json()
        assert data["detail"] == "Invalid token or user does not exist"

