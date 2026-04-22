import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.infrastructure.db_models import Base
from app.infrastructure.sql_repository import SQLItemRepository
from app.domain.item import ItemCreate, ItemUpdate


# Isolate tests with their own in-memory DB engine to avoid clashes
test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
TestingSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
def repo(session):
    return SQLItemRepository(session)


@pytest.mark.asyncio
async def test_add_item(repo):
    item_data = ItemCreate(name="Test Item", price=10.0, quantity=5)
    item = await repo.add(item_data)
    
    assert item.id is not None
    assert item.name == "Test Item"
    assert item.price == 10.0


@pytest.mark.asyncio
async def test_get_item(repo):
    item_data = ItemCreate(name="Test Item", price=10.0, quantity=5)
    added_item = await repo.add(item_data)
    
    fetched_item = await repo.get(added_item.id)
    assert fetched_item is not None
    assert fetched_item.id == added_item.id


@pytest.mark.asyncio
async def test_update_item(repo):
    item_data = ItemCreate(name="Test Item", price=10.0, quantity=5)
    added_item = await repo.add(item_data)
    
    update_data = ItemUpdate(price=20.0)
    updated_item = await repo.update(added_item.id, update_data)
    
    assert updated_item is not None
    assert updated_item.price == 20.0
    assert updated_item.name == "Test Item"
