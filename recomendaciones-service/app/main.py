
from fastapi import FastAPI

app = FastAPI(
    title="Microservicio de Recomendaciones",
    description="Sistema de recomendación de juegos de mesa",
    version="1.0.0"
)


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
