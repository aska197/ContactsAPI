import sys
import os

# Add the root directory of the project to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.repository import users
from app.db.models import User
from app.schemas import UserCreate
from app.core.auth import auth_service

class TestUserRepository(unittest.TestCase):
    
    @patch('app.repository.users.Gravatar')
    def test_create_user(self, MockGravatar):
        # Mock necessary dependencies
        mock_db = MagicMock(spec=Session)
        
        # Create a UserCreate instance (which UserModel extends)
        mock_user_create = UserCreate(username='johndoe', email='johndoe@example.com', password='secure')
        
        # Mock Gravatar
        mock_gravatar_instance = MockGravatar.return_value
        mock_gravatar_instance.get_image.return_value = 'http://example.com/avatar.jpg'

        # Call the function
        created_user = users.create_user(mock_user_create, mock_db)

        # Assertions
        self.assertEqual(created_user.username, 'johndoe')
        self.assertEqual(created_user.email, 'johndoe@example.com')
        self.assertEqual(created_user.avatar, 'http://example.com/avatar.jpg')
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(created_user)

    def test_get_user_by_email(self):
        # Mock necessary dependencies
        mock_db = MagicMock(spec=Session)
        mock_user = User(username='johndoe', email='johndoe@example.com')
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        # Call the function
        found_user = users.get_user_by_email('johndoe@example.com', mock_db)

        # Assertions
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.username, 'johndoe')
        self.assertEqual(found_user.email, 'johndoe@example.com')

    def test_get_user_by_username(self):
        # Mock necessary dependencies
        mock_db = MagicMock(spec=Session)
        mock_user = User(username='johndoe', email='johndoe@example.com')
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        # Call the function
        found_user = users.get_user_by_username(mock_db, 'johndoe')

        # Assertions
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.username, 'johndoe')
        self.assertEqual(found_user.email, 'johndoe@example.com')

    def test_update_token(self):
        # Mock necessary dependencies
        mock_db = MagicMock(spec=Session)
        mock_user = MagicMock(spec=User)

        # Call the function
        users.update_token(mock_user, 'new_token', mock_db)

        # Assertions
        self.assertEqual(mock_user.refresh_token, 'new_token')
        mock_db.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()



