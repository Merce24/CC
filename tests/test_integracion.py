import json
from urllib.request import urlopen


def obtener_respuesta(url):
    with urlopen(url, timeout=10) as respuesta:
        assert respuesta.status == 200
        return json.load(respuesta)


def test_usuarios_funcionando():
    datos = obtener_respuesta("http://localhost:8001/health")

    assert datos["estado"] == "ok"
    assert datos["servicio"] == "usuarios-service"


def test_catalogo_funcionando():
    datos = obtener_respuesta("http://localhost:8002/health")

    assert datos["estado"] == "ok"
    assert datos["servicio"] == "catalogo-service"


def test_recomendaciones_funcionando():
    datos = obtener_respuesta("http://localhost:8003/health")

    assert datos["estado"] == "ok"
    assert datos["servicio"] == "recomendaciones-service"


def test_conexion_bd_usuarios():
    datos = obtener_respuesta("http://localhost:8001/health/db")

    assert datos["estado"] == "ok"
    assert datos["conexion"] == "correcta"
    assert datos["base_datos"] == "postgres-usuarios"


def test_conexion_bd_catalogo():
    datos = obtener_respuesta("http://localhost:8002/health/db")

    assert datos["estado"] == "ok"
    assert datos["conexion"] == "correcta"
    assert datos["base_datos"] == "postgres-catalogo"
