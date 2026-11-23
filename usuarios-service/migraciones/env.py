
import os
from logging.config import fileConfig

from alembic import context
from app.models import Base
from sqlalchemy import create_engine, pool

# Configuración de Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)



target_metadata = Base.metadata


def obtener_url_bd():
    """Obtiene la conexión a PostgreSQL desde las variables de entorno."""

    url = os.getenv("DATABASE_URL")

    if not url:
        raise RuntimeError(
            "DATABASE_URL no está configurada"
        )

    # Utilizamos psycopg 3 como controlador de PostgreSQL
    if url.startswith("postgresql://"):
        url = url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1
        )

    return url


def run_migrations_offline():
    """Configura migraciones sin conexión activa a la base de datos."""

    context.configure(
        url=obtener_url_bd(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta las migraciones conectándose a PostgreSQL."""

    motor = create_engine(
        obtener_url_bd(),
        poolclass=pool.NullPool
    )

    try:
        with motor.connect() as conexion:
            context.configure(
                connection=conexion,
                target_metadata=target_metadata
            )

            with context.begin_transaction():
                context.run_migrations()
    finally:
        motor.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
