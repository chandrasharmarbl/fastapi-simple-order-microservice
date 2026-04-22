# FastAPI Simple Order Microservice

This repository contains a FastAPI microservice for managing items (a simplified order management system). It provides asynchronous CRUD operations for items and automatically dispatches event logs to a separate Analytics microservice whenever an item is created or modified.

## Features

- **Item Management**: Provides fully asynchronous endpoints to create and retrieve items.
- **Service-to-Service Communication**: Automatically sends non-blocking HTTP requests to an external Analytics microservice to log system events.
- **In-Memory Storage**: Uses a fast, in-memory dictionary to store items during the application's runtime.
- **Centralized Logging**: Outputs structured and consistent console logs for all application activities and external service failures.

## Getting Started

### Prerequisites

- Python 3.10+
- `pip`

### Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install the project along with its development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

Run the test suite using `pytest`:
```bash
pytest
```

### Starting the Services

To see the full service-to-service communication in action, you should run both the Items Microservice and the Analytics Microservice concurrently in separate terminal windows.

**Terminal 1: Start the Items Microservice**
```bash
uvicorn app.main:app --port 8000 --reload
```
Access the Swagger UI documentation for the Items API at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

**Terminal 2: Start the Analytics Microservice**
```bash
uvicorn analytics_service.app.main:app --port 8001 --reload
```
Access the Swagger UI documentation for the Analytics API at [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs).

## SOLID Refactoring & Dependency Inversion

As part of our continuous improvement, the project has been rigorously refactored to align with Clean Code and SOLID principles—specifically the **Dependency Inversion Principle**.

- The `ItemService` no longer depends on concrete repository implementations. It only depends on the `ItemRepositoryProtocol`.
- We utilize FastAPI's dependency injection (`Depends`) to dynamically inject our newly built `SQLItemRepository` when starting up the app, completely replacing the legacy `InMemoryItemRepository` without altering any logic inside `ItemService`.

## API curl Examples

Below are a few `curl` examples to demonstrate the service in action.

### 1. Create a New Item (POST)
```bash
curl -X POST "http://localhost:8000/api/v1/items" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Mechanical Keyboard",
           "price": 150.50,
           "quantity": 10
         }'
```

### 2. Fetch an Item (GET)
```bash
# Replace '1' with your returned item ID
curl -X GET "http://localhost:8000/api/v1/items/1"
```

### 3. Bulk Benchmark Operations (POST)
Compare ORM vs SQLAlchemy Core vs Raw SQL performance for 1000 items!
```bash
curl -X POST "http://localhost:8000/api/v1/benchmark/bulk" \
     -H "Content-Type: application/json" \
     -d '{"count": 1000}'
```

### 4. Application Health Check (GET)
```bash
curl -X GET "http://localhost:8000/health"
```
