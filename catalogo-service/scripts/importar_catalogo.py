"""Importa solo catálogo de un SQLite saneado a PostgreSQL.

Uso dentro de un contenedor catalogo con psycopg instalado:
  python /scripts/importar_catalogo.py --fuente /datos/catalogo_seed.db \
      --esquema /sql/001_catalogo.sql

La URL de PostgreSQL llega a través de la variable DATABASE_URL de Compose.
No se importa ninguna tabla de usuarios, comentarios, ludotecas o soporte.
"""

import argparse
import os
import sqlite3
from pathlib import Path

import psycopg
from psycopg import sql

TABLAS = (
    "categorias",
    "mecanicas",
    "juegos",
    "juego_categoria",
    "juego_mecanica",
)

COLUMNAS_JUEGOS = (
    "id_bgg",
    "nombre",
    "descripcion",
    "anio_publicacion",
    "min_jugadores",
    "max_jugadores",
    "duracion_minima",
    "duracion_maxima",
    "edad_minima",
    "valoracion_media",
    "complejidad",
    "imagen_url",
    "min_jugadores_recomendados",
    "max_jugadores_recomendados",
    "min_mejor_num_jugadores",
    "max_mejor_num_jugadores",
    "tipos_bgg",
    "ranking_general",
    "ranking_estrategia",
    "ranking_familiar",
    "ranking_tematico",
    "ranking_abstracto",
    "ranking_party",
    "ranking_wargame",
    "ranking_infantil",
)


def filas_sqlite(origen, tabla, columnas):
    """Lee las columnas indicadas sin depender del orden de SQLite."""
    consulta = 'SELECT {} FROM "{}"'.format(
        ", ".join('"{}"'.format(c) for c in columnas), tabla
    )
    return origen.execute(consulta).fetchall()


def upsert(cursor, tabla, columnas, conflicto, actualizar):
    """Construye inserciones parametrizadas con nombres SQL controlados."""
    cols = sql.SQL(", ").join(map(sql.Identifier, columnas))
    values = sql.SQL(", ").join(sql.Placeholder() for _ in columnas)
    if actualizar:
        sets = sql.SQL(", ").join(
            sql.SQL("{} = EXCLUDED.{}").format(sql.Identifier(c), sql.Identifier(c))
            for c in actualizar
        )
        action = sql.SQL("DO UPDATE SET {}").format(sets)
    else:
        action = sql.SQL("DO NOTHING")
    return sql.SQL("INSERT INTO {} ({}) VALUES ({}) ON CONFLICT ({}) {}").format(
        sql.Identifier(tabla),
        cols,
        values,
        sql.SQL(", ").join(map(sql.Identifier, conflicto)),
        action,
    )


def importar(fuente, esquema):
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise SystemExit("Error: falta DATABASE_URL; ejecuta mediante docker compose run")
    if not fuente.is_file() or not esquema.is_file():
        raise SystemExit("Error: no se encuentra la base de datos o el esquema SQL")

    origen = sqlite3.connect(f"file:{fuente}?mode=ro", uri=True)
    try:
        presentes = {
            fila[0]
            for fila in origen.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        if not set(TABLAS).issubset(presentes):
            raise SystemExit("Error: SQLite no contiene todas las tablas del catálogo")

        # Comprobación preventiva para no cargar asociaciones incoherentes.
        for tabla in ("juego_categoria", "juego_mecanica"):
            huerfanos = origen.execute(
                f"SELECT COUNT(*) FROM {tabla} AS j "
                "LEFT JOIN juegos AS g ON g.id_bgg = j.juego_id "
                "WHERE g.id_bgg IS NULL"
            ).fetchone()[0]
            if huerfanos:
                raise SystemExit(f"Error: {tabla} tiene {huerfanos} juegos inexistentes")

        configuracion = {
            "categorias": (("id", "nombre"), ("id",), ("nombre",)),
            "mecanicas": (("id", "nombre"), ("id",), ("nombre",)),
            "juegos": (
                COLUMNAS_JUEGOS,
                ("id_bgg",),
                tuple(c for c in COLUMNAS_JUEGOS if c != "id_bgg"),
            ),
            "juego_categoria": (
                ("juego_id", "categoria_id"), ("juego_id", "categoria_id"), ()
            ),
            "juego_mecanica": (
                ("juego_id", "mecanica_id"), ("juego_id", "mecanica_id"), ()
            ),
        }
        with psycopg.connect(dsn) as destino:
            with destino.cursor() as cursor:
                cursor.execute(esquema.read_text(encoding="utf-8"))
                for tabla, (columnas, conflicto, actualizar) in configuracion.items():
                    filas = filas_sqlite(origen, tabla, columnas)
                    cursor.executemany(
                        upsert(cursor, tabla, columnas, conflicto, actualizar), filas
                    )
                    print(f"{tabla}: {len(filas)} registros procesados")
                print("\nComprobación final en PostgreSQL:")
                for tabla in TABLAS:
                    cursor.execute(
                        sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(tabla))
                    )
                    total = cursor.fetchone()[0]
                    print(f"  {tabla}: {total}")
                # El contexto de conexión confirma los cambios solo si todo salió bien.
        print("\nImportación completada correctamente.")
    finally:
        origen.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fuente", type=Path, required=True)
    parser.add_argument("--esquema", type=Path, required=True)
    args = parser.parse_args()
    importar(args.fuente, args.esquema)


if __name__ == "__main__":
    main()
