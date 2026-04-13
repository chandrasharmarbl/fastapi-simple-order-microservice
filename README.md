# Order processing Project

The CRUD Service manages items with full Create, Read, Update, Delete operations, the Analytics Service logs all operations, and the Order Service creates orders by calling the CRUD Service. All services run independently on different ports and communicate via HTTP. The project includes a comprehensive test suite with TestClient that covers all endpoints and integrations without requiring running servers.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Activate the environment (if using virtual env):**
   ```bash
   source fastapienv/bin/activate
   ```

## Service Endpoints

### CRUD Service (Port 8000)
**Location:** `crud_service/app/`

- `POST /api/v1/items` - Create a new item
- `GET /api/v1/items` - List all items
- `GET /api/v1/items/{item_id}` - Get a specific item
- `PUT /api/v1/items/{item_id}` - Update an item
- `DELETE /api/v1/items/{item_id}` - Delete an item
- `GET /health` - Health check
- `GET /analytics` - Get analytics from Analytics Service

### Analytics Service (Port 8001)
**Location:** `analytics_service/app/`

- `POST /api/v1/log-event` - Log an event
- `GET /api/v1/events` - View all logged events
- `GET /api/v1/statistics` - View operation statistics
- `GET /health` - Health check

### Order Service (Port 8002)
**Location:** `client_service/app/`

- `POST /api/v1/orders` - Create an order
- `GET /api/v1/orders` - List all orders
- `GET /api/v1/orders/{order_id}` - Get a specific order
- `GET /api/v1/available-items` - Fetch available items from CRUD Service
- `GET /health` - Health check

## Running Services

```bash
# Terminal 1 - Analytics Service
cd analytics_service && python run.py

# Terminal 2 - CRUD Service
cd crud_service && python run.py

# Terminal 3 - Order Service
cd client_service && python run.py
```

## Running Tests

### Run all tests
```bash
pytest test_main.py -v
```

### Run tests with coverage
```bash
pytest test_main.py -v --cov=crud_service.app --cov=analytics_service.app --cov=client_service.app
```
