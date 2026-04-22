from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Using an async in-memory SQLite database for development
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create a session factory
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Declarative base for our models
class Base(DeclarativeBase):
    pass
