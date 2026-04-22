import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_benchmark_endpoint(client: AsyncClient):
    response = await client.post("/api/v1/benchmark/bulk", json={"count": 100})
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify the response contains timing comparisons
    assert "orm_time_ms" in data
    assert "core_time_ms" in data
    assert "raw_sql_time_ms" in data
    assert "total_records" in data
    assert data["total_records"] == 100
