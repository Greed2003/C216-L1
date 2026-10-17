from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services.item import (
    ItemAlreadyExistsError,
    ItemNotFoundError,
    ItemService,
)

router = APIRouter(prefix="/items", tags=["Items"])

DbSession = Annotated[Session, Depends(get_db)]


def get_service(db: DbSession) -> ItemService:
    return ItemService(ItemRepository(db))


ItemServiceDependency = Annotated[ItemService, Depends(get_service)]


@router.get("/", response_model=list[ItemRead])
def list_items(
    service: ItemServiceDependency,
    skip: int = 0,
    limit: int = 100,
):
    return service.list(skip, limit)


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, service: ItemServiceDependency):
    try:
        return service.get(item_id)
    except ItemNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado",
        ) from exc


@router.post(
    "/",
    response_model=ItemRead,
    status_code=status.HTTP_201_CREATED,
)
def create_item(item: ItemCreate, service: ItemServiceDependency):
    try:
        return service.create(item)
    except ItemAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item já existe",
        ) from exc


@router.put("/{item_id}", response_model=ItemRead)
def replace_item(
    item_id: int,
    item: ItemUpdate,
    service: ItemServiceDependency,
):
    try:
        return service.update(item_id, item)
    except ItemNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado",
        ) from exc
    except ItemAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item já existe",
        ) from exc


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int,
    item: ItemUpdate,
    service: ItemServiceDependency,
):
    try:
        return service.update(item_id, item)
    except ItemNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado",
        ) from exc
    except ItemAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item já existe",
        ) from exc


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item(item_id: int, service: ItemServiceDependency):
    try:
        service.delete(item_id)
    except ItemNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado",
        ) from exc
