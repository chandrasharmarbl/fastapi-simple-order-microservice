from typing import Optional
from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class Item(ItemCreate):
    id: int
