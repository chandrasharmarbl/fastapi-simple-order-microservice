from fastapi import Depends
from app.infrastructure.repository import InMemoryItemRepository
from app.infrastructure.analytics_client import AsyncAnalyticsClient
from app.services.item_service import ItemService

# Singletons to preserve state and connections across requests
_repository = InMemoryItemRepository()
_analytics_client = AsyncAnalyticsClient(base_url="http://localhost:8001")


def get_item_repository() -> InMemoryItemRepository:
    return _repository


def get_analytics_client() -> AsyncAnalyticsClient:
    return _analytics_client


def get_item_service(
    repository: InMemoryItemRepository = Depends(get_item_repository),
    analytics_client: AsyncAnalyticsClient = Depends(get_analytics_client)
) -> ItemService:
    return ItemService(repository=repository, analytics_client=analytics_client)
