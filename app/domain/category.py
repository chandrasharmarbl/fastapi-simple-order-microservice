from pydantic import BaseModel, ConfigDict
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class Category(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
