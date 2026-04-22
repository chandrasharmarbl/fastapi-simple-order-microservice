from typing import List, Optional, Protocol
from app.domain.item import ItemCreate, ItemUpdate, Item


class ItemRepositoryProtocol(Protocol):
    async def add(self, item_data: ItemCreate) -> Item:
        ...

    async def get(self, item_id: int) -> Optional[Item]:
        ...

    async def list(self) -> List[Item]:
        ...

    async def update(self, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
        ...

    async def delete(self, item_id: int) -> bool:
        ...
