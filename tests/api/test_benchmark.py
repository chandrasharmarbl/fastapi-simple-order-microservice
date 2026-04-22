import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.api.dependencies import get_db_session
from app.infrastructure.db_models import Base

# Setup test DB
test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
TestingSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db_session] = override_get_db_session

client = TestClient(app)

def test_benchmark_endpoint():
    response = client.post("/api/v1/benchmark/bulk", json={"count": 100})
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify the response contains timing comparisons
    assert "orm_time_ms" in data
    assert "core_time_ms" in data
    assert "raw_sql_time_ms" in data
    assert "total_records" in data
    assert data["total_records"] == 100
