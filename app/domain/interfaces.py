from typing import List, Optional, Protocol
from app.domain.item import ItemCreate, ItemUpdate, Item, ItemBulkUpdate


class ItemRepositoryProtocol(Protocol):
    async def add(self, item_data: ItemCreate) -> Item:
        ...

    async def get(self, item_id: int) -> Optional[Item]:
        ...

    async def list(self) -> List[Item]:
        ...

    async def update(self, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
        ...

    async def bulk_add(self, items: List[ItemCreate]) -> int:
        ...

    async def bulk_update(self, items: List[ItemBulkUpdate]) -> int:
        ...

    async def delete(self, item_id: int) -> bool:
        ...


class AnalyticsClientProtocol(Protocol):
    async def log_event(self, operation: str, item_id: int, item_name: str, details: str = "") -> None:
        ...
