
import os
from getpass import getpass

import psycopg
from argon2 import PasswordHasher


def crear_administrador():
    print("=== Crear administrador ===")

    nombre = input("Nombre: ").strip()
    email = input("Correo electrónico: ").strip().lower()

    if not nombre or not email or "@" not in email:
        print("Nombre o correo electrónico no válido.")
        return

    password = getpass("Contraseña: ")
    confirmacion = getpass("Repetir contraseña: ")

    if password != confirmacion:
        print("Las contraseñas no coinciden.")
        return

    if len(password) < 8:
        print("La contraseña debe tener al menos 8 caracteres.")
        return

    # Argon2 incorpora una sal aleatoria automáticamente
    password_hash = PasswordHasher().hash(password)

    with psycopg.connect(os.environ["DATABASE_URL"]) as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM usuarios WHERE email = %s",
                (email,),
            )

            if cursor.fetchone() is not None:
                print("Ya existe una cuenta con ese correo.")
                return

            cursor.execute(
                """
                INSERT INTO usuarios (
                    nombre,
                    email,
                    password_hash,
                    rol,
                    activo
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    nombre,
                    email,
                    password_hash,
                    "admin",
                    True,
                ),
            )

            usuario_id = cursor.fetchone()[0]

    print(f"Administrador creado correctamente. ID: {usuario_id}")


if __name__ == "__main__":
    crear_administrador()
