from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from async_generator import asynccontextmanager  # Import asynccontextmanager

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Define get_db as an asynchronous context manager
@asynccontextmanager
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
