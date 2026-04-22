from typing import List, Optional
from app.domain.item import ItemCreate, ItemUpdate, Item
from app.domain.interfaces import ItemRepositoryProtocol


class InMemoryItemRepository(ItemRepositoryProtocol):
    def __init__(self):
        self._storage: dict[int, Item] = {}
        self._next_id: int = 1

    async def add(self, item_data: ItemCreate) -> Item:
        item = Item(id=self._next_id, **item_data.model_dump())
        self._storage[self._next_id] = item
        self._next_id += 1
        return item

    async def get(self, item_id: int) -> Optional[Item]:
        return self._storage.get(item_id)

    async def list(self) -> List[Item]:
        return list(self._storage.values())

    async def update(self, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
        if item_id not in self._storage:
            return None
        existing_item = self._storage[item_id]
        update_data = item_data.model_dump(exclude_unset=True)
        updated_item = existing_item.model_copy(update=update_data)
        self._storage[item_id] = updated_item
        return updated_item

    async def delete(self, item_id: int) -> bool:
        if item_id in self._storage:
            del self._storage[item_id]
            return True
        return False
