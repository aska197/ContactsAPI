from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from app.core.config import settings
import asyncio
from pathlib import Path  # Import Path from pathlib module

class EmailSchema(BaseModel):
    email: EmailStr

# Define the necessary fields for ConnectionConfig based on your settings
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).resolve().parent.parent / 'templates',
)

def send_email(email: EmailSchema, token: str):
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email.email],
        body=f"Click on the link to verify your email: http://localhost:8000/api/auth/verify-email?token={token}",
        subtype="html"
    )
    fm = FastMail(conf)
    asyncio.run(fm.send_message(message))

