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


def test_item_update_optional_fields():
    item = ItemUpdate(price=15.0)
    assert item.name is None
    assert item.price == 15.0
    assert item.description is None
    assert item.quantity is None


def test_item_valid():
    item = Item(id=1, name="Test", price=10.0, quantity=5)
    assert item.id == 1
    assert item.name == "Test"
    assert item.quantity == 5
