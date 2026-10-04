from fastapi import APIRouter

from app.schemas.item import ItemCreate, ItemUpdate
from app.services.item import (
    create_item,
    delete_item,
    get_item,
    list_items,
    replace_item,
    update_item,
)

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/")
def list_items_endpoint(limit: int = 10):
    return list_items(limit)


@router.get("/{item_id}")
def get_item_endpoint(item_id: int):
    return get_item(item_id)


@router.post("/")
def create_item_endpoint(item: ItemCreate):
    return create_item(item)


@router.put("/{item_id}")
def replace_item_endpoint(item_id: int, item: ItemCreate):
    return replace_item(item_id, item)


@router.patch("/{item_id}")
def update_item_endpoint(item_id: int, item: ItemUpdate):
    return update_item(item_id, item)


@router.delete("/{item_id}")
def delete_item_endpoint(item_id: int):
    return delete_item(item_id)
