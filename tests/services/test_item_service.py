import pytest
from unittest.mock import AsyncMock
from app.domain.item import ItemCreate, Item
from app.services.item_service import ItemService


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.add.return_value = Item(id=1, name="Test Item", price=10.5, quantity=5)
    repo.get.return_value = Item(id=1, name="Test Item", price=10.5, quantity=5)
    return repo


@pytest.fixture
def mock_analytics():
    return AsyncMock()


@pytest.fixture
def item_service(mock_repo, mock_analytics):
    return ItemService(repository=mock_repo, analytics_client=mock_analytics)


@pytest.mark.asyncio
async def test_create_item(item_service, mock_repo, mock_analytics):
    item_data = ItemCreate(name="Test Item", price=10.5, quantity=5)
    
    result = await item_service.create_item(item_data)
    
    mock_repo.add.assert_called_once_with(item_data)
    
    mock_analytics.log_event.assert_called_once_with(
        operation="CREATE",
        item_id=1,
        item_name="Test Item",
        details="Created at price: 10.5, quantity: 5"
    )
    
    assert result.id == 1
    assert result.name == "Test Item"


@pytest.mark.asyncio
async def test_get_item(item_service, mock_repo, mock_analytics):
    result = await item_service.get_item(1)
    
    mock_repo.get.assert_called_once_with(1)
    # Reads should not trigger analytics logging based on original requirements
    mock_analytics.log_event.assert_not_called()
    
    assert result.id == 1
