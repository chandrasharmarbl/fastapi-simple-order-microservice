import pytest
from fastapi.testclient import TestClient
from crud_service.app.main import app
from crud_service.app.api.items import items_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_database():
    from crud_service.app.api import items
    items_db.clear()
    items.next_id = 1
    yield
    items_db.clear()


class TestHealthCheck:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["service"] == "Item CRUD Service"


class TestCreateItem:
    def test_create_item_success(self):
        payload = {
            "name": "Laptop",
            "description": "High-performance laptop",
            "price": 1200.0,
            "quantity": 5,
        }
        response = client.post("/api/v1/items", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Laptop"
        assert data["description"] == "High-performance laptop"
        assert data["price"] == 1200.0
        assert data["quantity"] == 5
    
    def test_create_item_minimal(self):
        payload = {
            "name": "Mouse",
            "price": 25.0,
        }
        response = client.post("/api/v1/items", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Mouse"
        assert data["description"] is None
        assert data["price"] == 25.0
        assert data["quantity"] == 0
    
    def test_create_multiple_items(self):
        items = [
            {"name": "Item1", "price": 10.0, "quantity": 5},
            {"name": "Item2", "price": 20.0, "quantity": 10},
            {"name": "Item3", "price": 30.0, "quantity": 3},
        ]
        
        ids = []
        for item in items:
            response = client.post("/api/v1/items", json=item)
            assert response.status_code == 201
            ids.append(response.json()["id"])
        
        assert ids == [1, 2, 3]


class TestListItems:
    def test_list_empty_items(self):
        response = client.get("/api/v1/items")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_items_with_data(self):
        for i in range(3):
            client.post("/api/v1/items", json={"name": f"Item{i+1}", "price": float(i+1) * 10, "quantity": i+5})
        
        response = client.get("/api/v1/items")
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 3
        assert items[0]["name"] == "Item1"
        assert items[2]["name"] == "Item3"


class TestGetItem:
    def test_get_existing_item(self):
        
        create_response = client.post(
            "/api/v1/items",
            json={"name": "Laptop", "description": "Gaming laptop", "price": 1500.0, "quantity": 8}
        )
        item_id = create_response.json()["id"]
        response = client.get(f"/api/v1/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == "Laptop"
        assert data["quantity"] == 8
    
    def test_get_nonexistent_item(self):
        response = client.get("/api/v1/items/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"


class TestUpdateItem:
    def test_update_all_fields(self):
        create_response = client.post(
            "/api/v1/items",
            json={"name": "Mouse", "description": "Old mouse", "price": 20.0, "quantity": 5}
        )
        item_id = create_response.json()["id"]
        update_payload = {
            "name": "Keyboard",
            "description": "Mechanical keyboard",
            "price": 150.0,
        }
        response = client.put(f"/api/v1/items/{item_id}", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == "Keyboard"
        assert data["description"] == "Mechanical keyboard"
        assert data["price"] == 150.0
        assert data["quantity"] == 5
    
    def test_update_partial_fields(self):
        create_response = client.post(
            "/api/v1/items",
            json={"name": "Headphones", "description": "Wireless", "price": 100.0, "quantity": 7}
        )
        item_id = create_response.json()["id"]
        response = client.put(f"/api/v1/items/{item_id}", json={"price": 85.0})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Headphones"
        assert data["description"] == "Wireless"
        assert data["price"] == 85.0
        assert data["quantity"] == 7
    
    def test_update_nonexistent_item(self):
        response = client.put("/api/v1/items/999", json={"name": "Updated"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"


class TestDeleteItem:
    def test_delete_existing_item(self):
        create_response = client.post("/api/v1/items", json={"name": "Temp Item", "price": 10.0, "quantity": 3})
        item_id = create_response.json()["id"]
        response = client.delete(f"/api/v1/items/{item_id}")
        assert response.status_code == 204
        get_response = client.get(f"/api/v1/items/{item_id}")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_item(self):
        response = client.delete("/api/v1/items/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"


class TestIntegration:
    def test_complete_crud_workflow(self):
        create_response = client.post(
            "/api/v1/items",
            json={"name": "Product", "description": "Test product", "price": 99.99, "quantity": 10}
        )
        assert create_response.status_code == 201
        item = create_response.json()
        item_id = item["id"]
        read_response = client.get(f"/api/v1/items/{item_id}")
        assert read_response.status_code == 200
        assert read_response.json()["name"] == "Product"
        update_response = client.put(
            f"/api/v1/items/{item_id}",
            json={"price": 79.99}
        )
        assert update_response.status_code == 200
        assert update_response.json()["price"] == 79.99
        delete_response = client.delete(f"/api/v1/items/{item_id}")
        assert delete_response.status_code == 204
        final_response = client.get(f"/api/v1/items/{item_id}")
        assert final_response.status_code == 404
    
    def test_multiple_items_workflow(self):
        items_data = [
            {"name": "Item1", "price": 10.0, "quantity": 5},
            {"name": "Item2", "price": 20.0, "quantity": 8},
            {"name": "Item3", "price": 30.0, "quantity": 3},
        ]
        created_ids = []
        for item_data in items_data:
            response = client.post("/api/v1/items", json=item_data)
            created_ids.append(response.json()["id"])
        list_response = client.get("/api/v1/items")
        assert len(list_response.json()) == 3
        client.delete(f"/api/v1/items/{created_ids[1]}")
        final_response = client.get("/api/v1/items")
        assert len(final_response.json()) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
