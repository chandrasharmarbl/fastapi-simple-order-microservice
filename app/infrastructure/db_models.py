from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from app.core.database import Base


class CategoryDB(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationship to Items
    items: Mapped[List["ItemDB"]] = relationship("ItemDB", back_populates="category")


class ItemDB(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)

    # Relationship to Category
    category: Mapped[Optional["CategoryDB"]] = relationship("CategoryDB", back_populates="items")
