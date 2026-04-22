import pytest
from pydantic import ValidationError
from app.domain.item import ItemCreate, ItemUpdate, Item


def test_item_create_valid():
    item = ItemCreate(name="Test Item", price=10.5)
    assert item.name == "Test Item"
    assert item.description is None
    assert item.price == 10.5
    assert item.quantity == 0


def test_item_create_invalid_price():
    with pytest.raises(ValidationError):
        ItemCreate(name="Test Item", price="invalid_price")


def test_item_update_ignore_unset():
    update_data = ItemUpdate(price=15.0)
    assert update_data.name is None
    assert update_data.price == 15.0
    assert update_data.quantity is None


def test_item_create_with_category():
    item = ItemCreate(name="Phone", price=500.0, quantity=10, category_id=1)
    assert item.category_id == 1

def test_item_with_category():
    item = Item(id=1, name="Phone", price=500.0, quantity=10, category_id=1)
    assert item.category_id == 1
    assert item.quantity == 10


def test_item_valid():
    item = Item(id=1, name="Test", price=10.0, quantity=5)
    assert item.id == 1
    assert item.name == "Test"
    assert item.quantity == 5
