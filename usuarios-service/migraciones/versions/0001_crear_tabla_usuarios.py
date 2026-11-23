
"""Crear tabla de usuarios.

Revision ID: 0001_usuarios
Revises:
"""

import sqlalchemy as sa
from alembic import op

revision = "0001_usuarios"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Crea la tabla usuarios."""

    op.create_table(
        "usuarios",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column(
            "nombre",
            sa.String(100),
            nullable=False,
        ),
        sa.Column(
            "email",
            sa.String(255),
            nullable=False,
        ),
        sa.Column(
            "password_hash",
            sa.String(255),
            nullable=False,
        ),
        sa.Column(
            "rol",
            sa.String(20),
            nullable=False,
            server_default="usuario",
        ),
        sa.Column(
            "activo",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    # Evita que dos usuarios tengan el mismo correo
    op.create_index(
        "ix_usuarios_email",
        "usuarios",
        ["email"],
        unique=True,
    )


def downgrade():
    """Revierte esta migración."""

    op.drop_index(
        "ix_usuarios_email",
        table_name="usuarios",
    )

    op.drop_table("usuarios")
