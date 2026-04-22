import time
from typing import Dict
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, text
from app.api.dependencies import get_db_session
from app.infrastructure.db_models import ItemDB


router = APIRouter(prefix="/api/v1/benchmark", tags=["benchmark"])


class BenchmarkRequest(BaseModel):
    count: int = 100


@router.post("/bulk", response_model=Dict[str, float])
async def benchmark_bulk(request: BenchmarkRequest, db: AsyncSession = Depends(get_db_session)):
    count = request.count
    data_list = [{"name": f"Benchmark Item {i}", "price": 15.0, "quantity": 1} for i in range(count)]
    
    # 1. ORM Bulk Insert
    start = time.perf_counter()
    db_items = [ItemDB(**data) for data in data_list]
    db.add_all(db_items)
    await db.commit()
    orm_time = (time.perf_counter() - start) * 1000
    
    # 2. Core Insert
    start = time.perf_counter()
    await db.execute(insert(ItemDB), data_list)
    await db.commit()
    core_time = (time.perf_counter() - start) * 1000
    
    # 3. Raw SQL Execution
    start = time.perf_counter()
    query = text("INSERT INTO items (name, price, quantity) VALUES (:name, :price, :quantity)")
    await db.execute(query, data_list)
    await db.commit()
    raw_sql_time = (time.perf_counter() - start) * 1000
    
    return {
        "orm_time_ms": round(orm_time, 2),
        "core_time_ms": round(core_time, 2),
        "raw_sql_time_ms": round(raw_sql_time, 2),
        "total_records": count
    }
