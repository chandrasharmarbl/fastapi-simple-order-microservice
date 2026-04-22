from typing import Optional
from app.domain.item import ItemCreate, Item
from app.domain.interfaces import ItemRepositoryProtocol, AnalyticsClientProtocol
from app.core.logger import get_logger


logger = get_logger(__name__)

class ItemService:
    def __init__(self, repository: ItemRepositoryProtocol, analytics_client: AnalyticsClientProtocol):
        self.repository = repository
        self.analytics_client = analytics_client

    async def create_item(self, item_data: ItemCreate) -> Item:
        logger.info(f"Creating new item: {item_data.name}")
        item = await self.repository.add(item_data)
        
        details = f"Created at price: {item.price}, quantity: {item.quantity}"
        
        await self.analytics_client.log_event(
            operation="CREATE",
            item_id=item.id,
            item_name=item.name,
            details=details
        )
        
        return item

    async def get_item(self, item_id: int) -> Optional[Item]:
        logger.info(f"Fetching item with ID: {item_id}")
        return await self.repository.get(item_id)
