import pytest
from app.domain.item import ItemCreate, ItemUpdate
from app.infrastructure.repository import InMemoryItemRepository


@pytest.fixture
def repo():
    return InMemoryItemRepository()


@pytest.mark.asyncio
async def test_add_item(repo):
    item_create = ItemCreate(name="Test", price=10.0)
    item = await repo.add(item_create)
    
    assert item.id == 1
    assert item.name == "Test"


@pytest.mark.asyncio
async def test_get_item(repo):
    item_create = ItemCreate(name="Test", price=10.0)
    await repo.add(item_create)
    
    item = await repo.get(1)
    assert item is not None
    assert item.name == "Test"


@pytest.mark.asyncio
async def test_get_nonexistent_item(repo):
    item = await repo.get(999)
    assert item is None


@pytest.mark.asyncio
async def test_list_items(repo):
    await repo.add(ItemCreate(name="Item 1", price=10.0))
    await repo.add(ItemCreate(name="Item 2", price=20.0))
    
    items = await repo.list()
    assert len(items) == 2
    assert items[0].name == "Item 1"


@pytest.mark.asyncio
async def test_update_item(repo):
    await repo.add(ItemCreate(name="Test", price=10.0))
    
    updated_item = await repo.update(1, ItemUpdate(price=15.0))
    assert updated_item is not None
    assert updated_item.price == 15.0
    assert updated_item.name == "Test"


@pytest.mark.asyncio
async def test_update_nonexistent_item(repo):
    updated_item = await repo.update(999, ItemUpdate(price=15.0))
    assert updated_item is None


@pytest.mark.asyncio
async def test_delete_item(repo):
    await repo.add(ItemCreate(name="Test", price=10.0))
    success = await repo.delete(1)
    
    assert success is True
    item = await repo.get(1)
    assert item is None


@pytest.mark.asyncio
async def test_delete_nonexistent_item(repo):
    success = await repo.delete(999)
    assert success is False
