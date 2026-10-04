from app.schemas.item import ItemCreate, ItemUpdate


def list_items(limit: int = 10):
    items = [
        {"id": 1, "name": "Item 1", "description": None},
        {"id": 2, "name": "Item 2", "description": None},
    ]
    return items[:limit]


def get_item(item_id: int):
    return {"id": item_id, "name": f"Item {item_id}", "description": None}


def create_item(item: ItemCreate):
    return {"id": 1, **item.model_dump()}


def replace_item(item_id: int, item: ItemCreate):
    return {"id": item_id, **item.model_dump()}


def update_item(item_id: int, item: ItemUpdate):
    return {"id": item_id, **item.model_dump(exclude_none=True)}


def delete_item(item_id: int):
    return {"deleted": item_id}
