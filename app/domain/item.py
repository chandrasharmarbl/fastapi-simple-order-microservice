from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.domain.category import Category


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

class ItemBulkUpdate(ItemUpdate):
    id: int


class Item(ItemCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ItemWithCategory(Item):
    category: Optional[Category] = None
