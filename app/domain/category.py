from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class Category(CategoryCreate):
    id: int
