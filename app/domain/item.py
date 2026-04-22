from typing import Optional
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    quantity: int = Field(0, ge=0)
    category_id: Optional[int] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None


class Item(ItemCreate):
    id: int
