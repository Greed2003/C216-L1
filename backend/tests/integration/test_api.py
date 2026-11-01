from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def unique_name(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def create_item(name: str):
    return client.post(
        "/items/",
        json={"name": name, "description": "Item de teste"},
    )


def test_root():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK


def test_create_item():
    response = create_item(unique_name("create"))

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] > 0

    client.delete(f"/items/{response.json()['id']}")


def test_list_items():
    created = create_item(unique_name("list"))
    item_id = created.json()["id"]

    response = client.get("/items/")

    assert response.status_code == status.HTTP_200_OK
    assert any(item["id"] == item_id for item in response.json())

    client.delete(f"/items/{item_id}")


def test_get_item():
    created = create_item(unique_name("get"))
    item_id = created.json()["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == item_id

    client.delete(f"/items/{item_id}")


def test_replace_item():
    created = create_item(unique_name("put"))
    item_id = created.json()["id"]
    new_name = unique_name("updated")

    response = client.put(
        f"/items/{item_id}",
        json={"name": new_name, "description": "Atualizado"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == new_name

    client.delete(f"/items/{item_id}")


def test_update_item():
    created = create_item(unique_name("patch"))
    item_id = created.json()["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={"description": "Atualização parcial"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["description"] == "Atualização parcial"

    client.delete(f"/items/{item_id}")


def test_delete_item():
    created = create_item(unique_name("delete"))
    item_id = created.json()["id"]

    response = client.delete(f"/items/{item_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(f"/items/{item_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
