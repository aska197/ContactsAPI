from typing import Optional, Union
from jose import JWTError, jwt
import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.config import settings
from app.repository import users as repository_users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class Auth:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = settings.ALGORITHM

    def verify_password(self, plain_password, hashed_password):
        """
        Verify if a plain password matches the hashed password.

        :param plain_password: The plain password to verify.
        :type plain_password: str
        :param hashed_password: The hashed password stored in the database.
        :type hashed_password: str
        :return: True if the plain password matches the hashed password, False otherwise.
        :rtype: bool
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def get_password_hash(self, password: str) -> str:
        """
        Generate a hashed password from a plain password.

        :param password: The plain password to hash.
        :type password: str
        :return: The hashed password.
        :rtype: str
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Create an access token with optional expiration.

        :param data: The data to encode into the token payload.
        :type data: dict
        :param expires_delta: Optional expiration time in seconds.
        :type expires_delta: float, optional
        :return: The encoded access token.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=150)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Create a refresh token with optional expiration.

        :param data: The data to encode into the token payload.
        :type data: dict
        :param expires_delta: Optional expiration time in seconds.
        :type expires_delta: float, optional
        :return: The encoded refresh token.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    def decode_refresh_token(self, refresh_token: str):
        """
        Decode and validate a refresh token.

        :param refresh_token: The refresh token to decode.
        :type refresh_token: str
        :raises HTTPException: If the token is invalid or has an invalid scope.
        :return: The email address associated with the refresh token.
        :rtype: str
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        Get the current user based on the access token.

        :param token: The access token obtained from the Authorization header.
        :type token: str
        :param db: The database session.
        :type db: Session
        :raises HTTPException: If the token is invalid or the user does not exist.
        :return: The current user.
        :rtype: User
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user

    def authenticate_user(self, db: Session, username: str, password: str):
        """
        Authenticate a user based on username and password.

        :param db: The database session.
        :type db: Session
        :param username: The username (email) of the user.
        :type username: str
        :param password: The user's password.
        :type password: str
        :return: The authenticated user if successful, False otherwise.
        :rtype: Union[User, bool]
        """
        user = repository_users.get_user_by_email(username, db)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

auth_service = Auth()



