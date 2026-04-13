from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Item, ItemCreate, ItemUpdate
from ..core.clients import log_to_analytics

router = APIRouter(prefix="/api/v1", tags=["items"])

items_db = {}
next_id = 1


@router.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    global next_id
    items_db[next_id] = {
        "id": next_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "quantity": item.quantity,
    }
    result = items_db[next_id]
    log_to_analytics(
        operation="CREATE",
        item_id=next_id,
        item_name=item.name,
        details=f"Created at price: ${item.price}, quantity: {item.quantity}"
    )
    next_id += 1
    return result


@router.get("/items", response_model=List[Item])
def list_items():
    return list(items_db.values())


@router.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    existing_item = items_db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)
    
    if "quantity" in update_data:
        new_quantity = existing_item["quantity"] + update_data["quantity"]
        if new_quantity < 0:
            raise HTTPException(status_code=400, detail="Quantity cannot be negative")
        update_data["quantity"] = new_quantity
    
    updated_item = {**existing_item, **update_data}
    items_db[item_id] = updated_item
    log_to_analytics(
        operation="UPDATE",
        item_id=item_id,
        item_name=updated_item["name"],
        details=f"Updated fields: {', '.join(update_data.keys())}"
    )
    return updated_item


@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item_name = items_db[item_id]["name"]
    del items_db[item_id]
    log_to_analytics(
        operation="DELETE",
        item_id=item_id,
        item_name=item_name,
        details="Item deleted"
    )
