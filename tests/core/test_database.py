import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.database import engine, async_session_maker, Base


def test_database_components_exist():
    assert isinstance(engine, AsyncEngine)
    assert issubclass(Base, DeclarativeBase)
    assert async_session_maker.kw["class_"] == AsyncSession
