from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from app.domain.item import ItemCreate, ItemUpdate, Item, ItemBulkUpdate
from app.domain.interfaces import ItemRepositoryProtocol
from app.infrastructure.db_models import ItemDB


class SQLItemRepository(ItemRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, item_data: ItemCreate) -> Item:
        db_item = ItemDB(**item_data.model_dump())
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return Item.model_validate(db_item)

    async def get(self, item_id: int) -> Optional[Item]:
        result = await self.session.execute(select(ItemDB).where(ItemDB.id == item_id))
        db_item = result.scalar_one_or_none()
        if db_item:
            return Item.model_validate(db_item)
        return None

    async def list(self) -> List[Item]:
        result = await self.session.execute(select(ItemDB))
        db_items = result.scalars().all()
        return [Item.model_validate(db_item) for db_item in db_items]

    async def update(self, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
        result = await self.session.execute(select(ItemDB).where(ItemDB.id == item_id))
        db_item = result.scalar_one_or_none()
        if not db_item:
            return None
        
        update_dict = item_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_item, key, value)
            
        await self.session.commit()
        await self.session.refresh(db_item)
        return Item.model_validate(db_item)

    async def bulk_add(self, items: List[ItemCreate]) -> int:
        if not items:
            return 0
        items_data = [item.model_dump() for item in items]
        await self.session.execute(insert(ItemDB), items_data)
        await self.session.commit()
        return len(items_data)

    async def bulk_update(self, items: List[ItemBulkUpdate]) -> int:
        if not items:
            return 0
        # For bulk updates, the dictionaries must include the primary key column name ('id')
        items_data = [item.model_dump(exclude_unset=True) for item in items]
        await self.session.execute(update(ItemDB), items_data)
        await self.session.commit()
        return len(items_data)
