
from fastapi import FastAPI, HTTPException
from psycopg import OperationalError

from app.database import comprobar_conexion_bd

app = FastAPI(
    title="Microservicio de Catálogo",
    description="Gestión del catálogo de juegos de mesa, mecánicas y categorías",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "servicio": "catalogo-service",
        "mensaje": "Microservicio de catálogo funcionando"
    }


@app.get("/health")
def comprobar_salud():
    return {
        "estado": "ok",
        "servicio": "catalogo-service"
    }


@app.get("/health/db")
def comprobar_base_datos():
    try:
        if comprobar_conexion_bd():
            return {
                "estado": "ok",
                "base_datos": "postgres-catalogo",
                "conexion": "correcta"
            }

    except (OperationalError, RuntimeError):
        pass

    raise HTTPException(
        status_code=503,
        detail="La base de datos no está disponible"
    )
