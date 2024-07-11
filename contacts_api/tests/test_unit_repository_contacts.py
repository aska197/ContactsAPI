import sys
import os

# Add the root directory of the project to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest import TestCase, mock
from datetime import datetime
from sqlalchemy.orm import Session
from app.repository import contacts
from app.schemas import ContactCreate, User
from app.db.models import Contact

class TestContactRepository(TestCase):

    @mock.patch('app.repository.contacts.get_contact')
    def test_get_contact(self, mock_get_contact):
        mock_db = mock.Mock(spec=Session)
        mock_user = User(id=1, username="testuser", email="testuser@example.com", created_at=datetime.now())
        mock_contact = Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com", phone_number="1234567890", birthday=datetime(1990, 1, 1), user_id=1)
        mock_get_contact.return_value = mock_contact
        result = contacts.get_contact(mock_db, 1, mock_user)
        mock_get_contact.assert_called_once_with(mock_db, 1, mock_user)
        self.assertEqual(result, mock_contact)

    @mock.patch('app.repository.contacts.get_contacts')
    def test_get_contacts(self, mock_get_contacts):
        mock_db = mock.Mock(spec=Session)
        mock_user = User(id=1, username="testuser", email="testuser@example.com", created_at=datetime.now())
        mock_contacts = [
            Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com", phone_number="1234567890", birthday=datetime(1990, 1, 1), user_id=1),
            Contact(id=2, first_name="Jane", last_name="Smith", email="jane.smith@example.com", phone_number="9876543210", birthday=datetime(1995, 5, 15), user_id=1)
        ]
        mock_get_contacts.return_value = mock_contacts
        results = contacts.get_contacts(mock_db, mock_user, skip=0, limit=10)
        mock_get_contacts.assert_called_once_with(mock_db, mock_user, skip=0, limit=10)
        self.assertEqual(results, mock_contacts)

    @mock.patch('app.repository.contacts.create_contact')
    def test_create_contact(self, mock_create_contact):
        mock_db = mock.Mock(spec=Session)
        mock_user = User(id=1, username="testuser", email="testuser@example.com", created_at=datetime.now())
        mock_contact_create = ContactCreate(first_name="John", last_name="Doe", email="john.doe@example.com", phone_number="1234567890", birthday=datetime(1990, 1, 1))
        mock_created_contact = Contact(id=1, **mock_contact_create.dict(), user_id=mock_user.id)
        mock_create_contact.return_value = mock_created_contact
        result = contacts.create_contact(mock_db, mock_contact_create, mock_user)
        mock_create_contact.assert_called_once_with(mock_db, mock_contact_create, mock_user)
        self.assertEqual(result.id, 1)

    @mock.patch('app.repository.contacts.update_contact')
    def test_update_contact(self, mock_update_contact):
        mock_db = mock.Mock(spec=Session)
        mock_user = User(id=1, username="testuser", email="testuser@example.com", created_at=datetime.now())
        mock_contact_update = ContactCreate(first_name="Jane", last_name="Smith", email="jane.smith@example.com", phone_number="9876543210", birthday=datetime(1995, 5, 15))
        mock_updated_contact = Contact(id=1, **mock_contact_update.dict(), user_id=mock_user.id)
        mock_update_contact.return_value = mock_updated_contact
        updated_contact = contacts.update_contact(mock_db, 1, mock_contact_update, mock_user)
        mock_update_contact.assert_called_once_with(mock_db, 1, mock_contact_update, mock_user)
        self.assertEqual(updated_contact.phone_number, "9876543210")

    @mock.patch('app.repository.contacts.get_contact')
    def test_delete_contact(self, mock_get_contact):
        mock_db = mock.Mock(spec=Session)
        mock_user = User(id=1, username="testuser", email="testuser@example.com", created_at=datetime.now())
        mock_contact = Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com", phone_number="1234567890", birthday=datetime(1990, 1, 1), user_id=1)
        mock_get_contact.return_value = mock_contact
        
        print("Calling delete_contact function")
        result = contacts.delete_contact(mock_db, 1, mock_user)
        
        print("Asserting mock_get_contact called once")
        mock_get_contact.assert_called_once_with(mock_db, 1, mock_user)
        mock_db.delete.assert_called_once_with(mock_contact)
        mock_db.commit.assert_called_once()
        self.assertEqual(result, mock_contact)
        
if __name__ == '__main__':
    unittest.main()
