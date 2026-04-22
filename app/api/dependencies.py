from fastapi import Depends
from app.domain.interfaces import ItemRepositoryProtocol, AnalyticsClientProtocol
from app.infrastructure.repository import InMemoryItemRepository
from app.infrastructure.sql_repository import SQLItemRepository
from app.infrastructure.analytics_client import AsyncAnalyticsClient
from app.services.item_service import ItemService
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from app.core.database import async_session_maker

# Singletons for memory repositories and clients
_memory_repository = InMemoryItemRepository()
_analytics_client = AsyncAnalyticsClient(base_url="http://localhost:8001")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_sql_item_repository(session: AsyncSession = Depends(get_db_session)) -> ItemRepositoryProtocol:
    return SQLItemRepository(session)


def get_analytics_client() -> AnalyticsClientProtocol:
    return _analytics_client


def get_item_service(
    # DEPENDENCY INVERSION: Depending on Protocol instead of Concrete Class
    repository: ItemRepositoryProtocol = Depends(get_sql_item_repository),
    analytics_client: AnalyticsClientProtocol = Depends(get_analytics_client)
) -> ItemService:
    return ItemService(repository=repository, analytics_client=analytics_client)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
