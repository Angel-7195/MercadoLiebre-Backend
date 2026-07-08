from __future__ import annotations

from typing import Any

from app.crud.http_client import APIClient


def list_shopping(client: APIClient) -> list[dict[str, Any]]:
    response = client.get("/api/shopping")
    response.raise_for_status()
    return response.json()


def get_shopping(client: APIClient, shopping_id: str) -> dict[str, Any]:
    response = client.get(f"/api/shopping/{shopping_id}")
    response.raise_for_status()
    return response.json()


def create_shopping(
    client: APIClient,
    *,
    user_id: str,
    total_amount: float,
    status: str,
) -> dict[str, Any]:
    response = client.post(
        "/api/shopping",
        json={
            "user_id": user_id,
            "total_amount": total_amount,
            "status": status,
        },
    )
    response.raise_for_status()
    return response.json()


def update_shopping(
    client: APIClient,
    shopping_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    response = client.put(f"/api/shopping/{shopping_id}", json=payload)
    response.raise_for_status()
    return response.json()


def delete_shopping(client: APIClient, shopping_id: str) -> None:
    response = client.delete(f"/api/shopping/{shopping_id}")
    response.raise_for_status()