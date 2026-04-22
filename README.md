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
