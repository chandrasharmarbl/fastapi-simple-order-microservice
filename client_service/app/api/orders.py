from fastapi import APIRouter, HTTPException
import requests
from datetime import datetime
from ..models import Order, OrderCreate

router = APIRouter(prefix="/api/v1", tags=["orders"])

ITEM_SERVICE_URL = "http://localhost:8000"

orders_db = {}
next_order_id = 1


@router.post("/orders", response_model=Order, status_code=201)
def create_order(order_create: OrderCreate):
    global next_order_id
    
    try:
        total_price = 0.0
        order_details = []
        
        for order_item in order_create.items:
            response = requests.get(f"{ITEM_SERVICE_URL}/api/v1/items/{order_item.item_id}", timeout=2)
            response.raise_for_status()
            item = response.json()
            
            if item["quantity"] < order_item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Item '{item['name']}' has only {item['quantity']} in stock, but {order_item.quantity} requested"
                )
            
            item_total = item["price"] * order_item.quantity
            total_price += item_total
            
            order_details.append({
                "item_id": order_item.item_id,
                "item_name": item["name"],
                "quantity": order_item.quantity,
                "price_per_unit": item["price"],
                "subtotal": item_total
            })
        
        for order_item in order_create.items:
            requests.put(
                f"{ITEM_SERVICE_URL}/api/v1/items/{order_item.item_id}",
                json={"quantity": -order_item.quantity},
                timeout=2
            )
        
        order = {
            "id": next_order_id,
            "items": order_create.items,
            "total_price": total_price,
            "created_at": datetime.now().isoformat(),
            "details": order_details
        }
        orders_db[next_order_id] = order
        next_order_id += 1
        
        return order
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Could not reach Item Service: {str(e)}")


@router.get("/orders")
def list_orders():
    return list(orders_db.values())


@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]


@router.get("/available-items")
def get_available_items():
    try:
        response = requests.get(f"{ITEM_SERVICE_URL}/api/v1/items", timeout=2)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Could not reach Item Service: {str(e)}")
