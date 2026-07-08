from __future__ import annotations

"""
Descripción:
    Este archivo contiene las funciones encargadas de consumir los endpoints
    de autenticación de la API MercadoLiebre mediante peticiones HTTP.

    Su objetivo es permitir que el cliente (menú por consola) pueda iniciar
    sesión y obtener un token JWT que será utilizado para acceder a los
    endpoints protegidos de la aplicación.
"""

from typing import Any

from app.crud.http_client import APIClient


# -----------------------------------------------------------------------------
# Realiza el inicio de sesión de un usuario.
#
# Envía una petición HTTP POST al endpoint:
#     POST /api/auth/login
#
# Parámetros:
#     email    -> Correo electrónico del usuario.
#     password -> Contraseña del usuario.
#
# La API devuelve un token JWT que será utilizado en las siguientes peticiones
# para autenticar al usuario.
# -----------------------------------------------------------------------------
def login(
    client: APIClient,
    *,
    email: str,
    password: str,
) -> dict[str, Any]:

    # OAuth2PasswordRequestForm espera recibir los campos
    # "username" y "password". En este proyecto utilizamos el
    # correo electrónico como nombre de usuario.
    data = {
        "username": email,
        "password": password,
    }

    # Enviar la petición al endpoint de autenticación.
    response = client.client.post(
        "/api/auth/login",
        data=data,
    )

    # Si ocurre un error HTTP (401, 404, 500, etc.)
    # se lanza automáticamente una excepción.
    response.raise_for_status()

    # Retornar la respuesta de la API en formato JSON.
    return response.json()