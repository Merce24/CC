
from fastapi.testclient import TestClient
from app.main import app

cliente = TestClient(app)


def test_inicio():
    respuesta = cliente.get("/")

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "servicio": "recomendaciones-service",
        "mensaje": "Microservicio de recomendaciones funcionando"
    }


def test_health():
    respuesta = cliente.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "estado": "ok",
        "servicio": "recomendaciones-service"
    }
