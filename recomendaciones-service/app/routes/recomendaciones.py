
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["Recomendaciones"],
)


class SolicitudRecomendacion(BaseModel):
    jugadores_min: int = Field(ge=1, le=50)
    jugadores_max: int | None = Field(default=None, ge=1, le=50)
    duracion_maxima: int | None = Field(default=None, gt=0)
    complejidad_maxima: float | None = Field(
        default=None, ge=0, le=5
    )
    limite: int = Field(default=10, ge=1, le=50)


def obtener_catalogo():
    """Obtiene todos los juegos mediante la API de Catálogo."""

    url_base = os.environ["CATALOGO_URL"].rstrip("/")
    juegos = []
    pagina = 1

    try:
        while True:
            parametros = urlencode({
                "page": pagina,
                "limit": 100,
            })

            url = f"{url_base}/api/v1/games?{parametros}"

            with urlopen(url, timeout=10) as respuesta:
                datos = json.load(respuesta)

            lote = datos["juegos"]
            juegos.extend(lote)

            if not lote or pagina * 100 >= datos["total"]:
                break

            pagina += 1

    except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar el catálogo",
        ) from error

    return juegos


@router.post("")
def recomendar(solicitud: SolicitudRecomendacion):
    """Recomienda juegos según las restricciones indicadas."""

    minimo = solicitud.jugadores_min
    maximo = solicitud.jugadores_max or minimo

    if maximo < minimo:
        raise HTTPException(
            status_code=422,
            detail="jugadores_max no puede ser menor que jugadores_min",
        )

    juegos = obtener_catalogo()
    candidatos = []

    for juego in juegos:
        min_j = juego["min_jugadores"]
        max_j = juego["max_jugadores"]

        # El juego debe admitir el rango de jugadores solicitado
        if min_j is None or max_j is None:
            continue

        if min_j > minimo or max_j < maximo:
            continue

        duracion = juego["duracion_maxima"]
        complejidad = juego["complejidad"]

        if solicitud.duracion_maxima is not None and (
            duracion is None or duracion > solicitud.duracion_maxima
        ):
            continue

        if solicitud.complejidad_maxima is not None and (
            complejidad is None or complejidad > solicitud.complejidad_maxima
        ):
            continue

        valoracion = float(juego["valoracion_media"] or 0)

        motivos = [
            f"Adecuado para {minimo} a {maximo} jugadores"
        ]

        if solicitud.duracion_maxima is not None:
            motivos.append("Duración compatible")

        if solicitud.complejidad_maxima is not None:
            motivos.append("Complejidad compatible")

        candidatos.append({
            "id_bgg": juego["id_bgg"],
            "nombre": juego["nombre"],
            "min_jugadores": min_j,
            "max_jugadores": max_j,
            "duracion_maxima": duracion,
            "complejidad": complejidad,
            "valoracion_media": juego["valoracion_media"],
            "puntuacion": valoracion,
            "motivos": motivos,
        })

    # Primera versión: ordenar por valoración media
    candidatos.sort(
        key=lambda juego: juego["puntuacion"],
        reverse=True,
    )

    return {
        "total_candidatos": len(candidatos),
        "resultados": candidatos[:solicitud.limite],
    }
