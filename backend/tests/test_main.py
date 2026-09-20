import pytest
from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def soma(a, b):
    return a + b


def eh_par(numero):
    return numero % 2 == 0


def dividir(a, b):
    if b == 0:
        raise ValueError("divisão por zero")

    return a / b


@pytest.fixture
def usuario():
    return {
        "nome": "Maria",
        "email": "maria@example.com",
    }


def test_soma():
    assert soma(2, 3) == 5


def test_numero_par():
    assert eh_par(4) is True


def test_divisao():
    assert dividir(10, 2) == 5


def test_divisao_por_zero():
    with pytest.raises(ValueError):
        dividir(10, 0)


@pytest.mark.parametrize(
    "numero, esperado",
    [
        (2, True),
        (3, False),
        (10, True),
        (11, False),
    ],
)
def test_eh_par(numero, esperado):
    assert eh_par(numero) is esperado


def test_nome_usuario(usuario):
    assert usuario["nome"] == "Maria"


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Olá, Sistemas Distribuídos!"}
