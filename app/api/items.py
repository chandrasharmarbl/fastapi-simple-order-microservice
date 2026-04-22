from fastapi import APIRouter, Depends, HTTPException
from app.domain.item import ItemCreate, Item
from app.services.item_service import ItemService
from app.api.dependencies import get_item_service

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.post("", response_model=Item, status_code=201)
async def create_item(
    item_data: ItemCreate, 
    service: ItemService = Depends(get_item_service)
):
    return await service.create_item(item_data)


@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: int, 
    service: ItemService = Depends(get_item_service)
):
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
