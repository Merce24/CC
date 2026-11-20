
import os

import psycopg


def comprobar_conexion_bd():
    url = os.getenv("DATABASE_URL")

    if not url:
        raise RuntimeError("DATABASE_URL no está configurada")

    with (
        psycopg.connect(url, connect_timeout=5) as conexion,
        conexion.cursor() as cursor,
    ):
        cursor.execute("SELECT 1")
        resultado = cursor.fetchone()

    return resultado[0] == 1
