
import os

import psycopg
from fastapi import APIRouter, HTTPException, Query
from psycopg.rows import dict_row

router = APIRouter(prefix="/api/v1/games", tags=["Juegos"])


@router.get("")
def listar_juegos(
    query: str | None = Query(default=None, max_length=100),
    players: int | None = Query(default=None, ge=1, le=50),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
):
    condiciones = []
    parametros = []

    if query:
        condiciones.append("nombre ILIKE %s")
        parametros.append(f"%{query}%")

    if players is not None:
        condiciones.append(
            "min_jugadores <= %s AND max_jugadores >= %s"
        )
        parametros.extend([players, players])

    where = ""
    if condiciones:
        where = "WHERE " + " AND ".join(condiciones)

    offset = (page - 1) * limit

    with psycopg.connect(
        os.environ["DATABASE_URL"],
        row_factory=dict_row,
    ) as conexion, conexion.cursor() as cursor:
        cursor.execute(
            f"SELECT COUNT(*) AS total FROM juegos {where}",
            parametros,
        )
        total = cursor.fetchone()["total"]

        cursor.execute(
            f"""
                SELECT
                    id_bgg,
                    nombre,
                    anio_publicacion,
                    min_jugadores,
                    max_jugadores,
                    duracion_minima,
                    duracion_maxima,
                    valoracion_media,
                    complejidad,
                    imagen_url
                FROM juegos
                {where}
                ORDER BY nombre, id_bgg
                LIMIT %s OFFSET %s
                """,
            parametros + [limit, offset],
        )
        juegos = cursor.fetchall()

    return {
        "total": total,
        "pagina": page,
        "limite": limit,
        "juegos": juegos,
    }


@router.get("/{bgg_id}")
def obtener_juego(bgg_id: int):
    """Obtiene la ficha completa de un juego por su ID de BGG."""

    with psycopg.connect(
        os.environ["DATABASE_URL"],
        row_factory=dict_row,
    ) as conexion, conexion.cursor() as cursor:

        # Información principal del juego
        cursor.execute(
            """
                SELECT *
                FROM juegos
                WHERE id_bgg = %s
                """,
            (bgg_id,),
        )

        juego = cursor.fetchone()

        if juego is None:
            raise HTTPException(
                status_code=404,
                detail="Juego no encontrado",
            )

        # Mecánicas asociadas al juego
        cursor.execute(
            """
                SELECT m.id, m.nombre
                FROM mecanicas m
                JOIN juego_mecanica jm
                    ON jm.mecanica_id = m.id
                WHERE jm.juego_id = %s
                ORDER BY m.nombre
                """,
            (bgg_id,),
        )

        mecanicas = cursor.fetchall()

        # Categorías asociadas al juego
        cursor.execute(
            """
                SELECT c.id, c.nombre
                FROM categorias c
                JOIN juego_categoria jc
                    ON jc.categoria_id = c.id
                WHERE jc.juego_id = %s
                ORDER BY c.nombre
                """,
            (bgg_id,),
        )

        categorias = cursor.fetchall()

    return {
        **juego,
        "mecanicas": mecanicas,
        "categorias": categorias,
    }
