from __future__ import annotations

from typing import Any

from app.crud.http_client import APIClient


# -----------------------------------------------------------------------------
# CRUD de Users
#
# Este archivo contiene las funciones que consumen la API REST mediante
# peticiones HTTP.
#
# No interactúa directamente con la base de datos.
# Cada función envía una solicitud al backend de FastAPI utilizando la clase
# APIClient.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Obtiene la lista completa de usuarios.
#
# Realiza una petición:
#     GET /api/users
#
# Retorna:
#     Una lista de diccionarios con la información de cada usuario.
# -----------------------------------------------------------------------------
def list_users(client: APIClient) -> list[dict[str, Any]]:
    r = client.get("/api/users")

    # Si ocurre un error HTTP (404, 500, etc.)
    # se lanza automáticamente una excepción.
    r.raise_for_status()

    return r.json()


# -----------------------------------------------------------------------------
# Obtiene un usuario específico utilizando su UUID.
#
# Realiza una petición:
#     GET /api/users/{user_id}
#
# Parámetros:
#     user_id -> UUID del usuario.
#
# Retorna:
#     Un diccionario con la información del usuario.
# -----------------------------------------------------------------------------
def get_user(
    client: APIClient,
    user_id: str,
) -> dict[str, Any]:

    r = client.get(f"/api/users/{user_id}")

    r.raise_for_status()

    return r.json()


# -----------------------------------------------------------------------------
# Crea un nuevo usuario.
#
# Realiza una petición:
#     POST /api/users
#
# Parámetros:
#     payload -> Diccionario con los datos del nuevo usuario.
#
# Retorna:
#     El usuario creado por la API.
# -----------------------------------------------------------------------------
def create_user(
    client: APIClient,
    payload: dict[str, Any],
) -> dict[str, Any]:

    r = client.post(
        "/api/users",
        json=payload,
    )

    r.raise_for_status()

    return r.json()


# -----------------------------------------------------------------------------
# Actualiza un usuario existente.
#
# Realiza una petición:
#     PUT /api/users/{user_id}
#
# Parámetros:
#     user_id -> UUID del usuario.
#     payload -> Campos que se desean modificar.
#
# Retorna:
#     El usuario actualizado.
# -----------------------------------------------------------------------------
def update_user(
    client: APIClient,
    user_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:

    r = client.put(
        f"/api/users/{user_id}",
        json=payload,
    )

    r.raise_for_status()

    return r.json()


# -----------------------------------------------------------------------------
# Elimina un usuario.
#
# Realiza una petición:
#     DELETE /api/users/{user_id}
#
# Parámetros:
#     user_id -> UUID del usuario que se desea eliminar.
#
# La API responde con código HTTP 204 (No Content) cuando la operación
# se realiza correctamente.
# -----------------------------------------------------------------------------
def delete_user(
    client: APIClient,
    user_id: str,
) -> None:

    r = client.delete(f"/api/users/{user_id}")

    r.raise_for_status()