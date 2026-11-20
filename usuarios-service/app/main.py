from fastapi import FastAPI
from fastapi import HTTPException
from psycopg import OperationalError

from app.database import comprobar_conexion_bd

app = FastAPI(
    title="Microservicio de Usuarios y Ludotecas",
    description="Gestión de usuarios, autenticación y ludotecas",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "servicio": "usuarios-service",
        "mensaje": "Microservicio de usuarios funcionando"
    }


@app.get("/health")
def comprobar_salud():
    return {
        "estado": "ok",
        "servicio": "usuarios-service"
    }


@app.get("/health/db")
def comprobar_base_datos():
    try:
        if comprobar_conexion_bd():
            return {
                "estado": "ok",
                "base_datos": "postgres-usuarios",
                "conexion": "correcta"
            }
    except (OperationalError, RuntimeError):
        pass

    raise HTTPException(
        status_code=503,
        detail="La base de datos no está disponible"
    )
