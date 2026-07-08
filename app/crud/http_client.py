from __future__ import annotations

from typing import Any

import httpx


class APIClient:
    """
    Cliente HTTP que permite comunicarse con la API REST.

    Centraliza las peticiones GET, POST, PUT y DELETE para que
    el resto del proyecto no tenga que repetir código.
    """

    def __init__(self, base_url: str) -> None:
        # Guarda la URL base de la API.
        # rstrip("/") elimina una barra "/" al final si existe para evitar
        # problemas al construir las rutas.
        self.base_url = base_url.rstrip("/")

        # Crea el cliente HTTP con un tiempo máximo de espera de 15 segundos.
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=15,
        )

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """
        Realiza una petición GET para consultar información.
        """
        return self.client.get(path, params=params)

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """
        Realiza una petición POST para crear nuevos registros.
        """
        return self.client.post(path, json=json, params=params)

    def put(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """
        Realiza una petición PUT para actualizar un registro existente.
        """
        return self.client.put(path, json=json, params=params)

    def delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """
        Realiza una petición DELETE para eliminar un registro.
        """
        return self.client.delete(path, params=params)

    def close(self) -> None:
        """
        Cierra la conexión del cliente HTTP para liberar recursos.
        """
        self.client.close()

    def set_bearer_token(self, token: str) -> None:
        """
        Agrega el token JWT al encabezado Authorization.

        Esto permite acceder a los endpoints protegidos
        que requieren autenticación.
        """
        if token:
            self.client.headers.update(
                {"Authorization": f"Bearer {token}"}
            )