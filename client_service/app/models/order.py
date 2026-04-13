from pydantic import BaseModel
from typing import List


class OrderItem(BaseModel):
    item_id: int
    quantity: int


class Order(BaseModel):
    id: int
    items: List[OrderItem]
    total_price: float
    created_at: str


class OrderCreate(BaseModel):
    items: List[OrderItem]
