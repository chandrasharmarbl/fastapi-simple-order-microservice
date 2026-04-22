import pytest
from sqlalchemy import inspect
from app.infrastructure.db_models import ItemDB, CategoryDB


def test_category_db_model():
    mapper = inspect(CategoryDB)
    assert mapper.local_table.name == "categories"
    
    columns = [c.name for c in mapper.columns]
    assert "id" in columns
    assert "name" in columns
    assert "description" in columns


def test_item_db_model():
    mapper = inspect(ItemDB)
    assert mapper.local_table.name == "items"
    
    columns = [c.name for c in mapper.columns]
    assert "id" in columns
    assert "name" in columns
    assert "description" in columns
    assert "price" in columns
    assert "quantity" in columns
    assert "category_id" in columns
    
    # Check relationship
    assert "category" in mapper.relationships
