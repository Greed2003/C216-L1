from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Olá, Sistemas Distribuídos!"}


def test_list_items():
    response = client.get("/items/?limit=1")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


def test_get_item():
    response = client.get("/items/10")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 10


def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Item novo", "description": "Descrição"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Item novo"


def test_replace_item():
    response = client.put(
        "/items/10",
        json={"name": "Item atualizado", "description": "Nova descrição"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 10
    assert response.json()["name"] == "Item atualizado"


def test_update_item():
    response = client.patch(
        "/items/10",
        json={"name": "Item parcial"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 10
    assert response.json()["name"] == "Item parcial"


def test_delete_item():
    response = client.delete("/items/10")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"deleted": 10}
