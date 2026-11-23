
from fastapi import FastAPI

from app.routes.recomendaciones import router as recomendaciones_router

app = FastAPI(
    title="Microservicio de Recomendaciones",
    description="Sistema de recomendación de juegos de mesa",
    version="1.0.0"
)

app.include_router(recomendaciones_router)


@app.get("/")
def inicio():
    return {
        "servicio": "recomendaciones-service",
        "mensaje": "Microservicio de recomendaciones funcionando"
    }


@app.get("/health")
def comprobar_salud():
    return {
        "estado": "ok",
        "servicio": "recomendaciones-service"
    }
