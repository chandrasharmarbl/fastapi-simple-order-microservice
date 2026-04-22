import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.main import app
from app.domain.item import Item
from app.api.dependencies import get_item_service


# Setup the mock service
mock_service = AsyncMock()


def override_get_item_service():
    return mock_service


# Override the dependency in the FastAPI app
app.dependency_overrides[get_item_service] = override_get_item_service

client = TestClient(app)


def test_create_item_endpoint():
    # Setup mock behavior
    mock_service.create_item.return_value = Item(id=1, name="Test Endpoint", price=20.0, quantity=2)
    
    response = client.post(
        "/api/v1/items",
        json={"name": "Test Endpoint", "price": 20.0, "quantity": 2}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Endpoint"


def test_get_item_endpoint():
    # Setup mock behavior
    mock_service.get_item.return_value = Item(id=1, name="Test Endpoint", price=20.0, quantity=2)
    
    response = client.get("/api/v1/items/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Endpoint"


def test_get_nonexistent_item_endpoint():
    # Setup mock behavior
    mock_service.get_item.return_value = None
    
    response = client.get("/api/v1/items/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
