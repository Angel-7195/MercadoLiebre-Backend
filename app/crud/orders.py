from __future__ import annotations

from typing import Any

from app.crud.http_client import APIClient


def list_orders(client: APIClient) -> list[dict[str, Any]]:
    response = client.get("/api/orders")
    response.raise_for_status()
    return response.json()


def get_order(client: APIClient, order_id: str) -> dict[str, Any]:
    response = client.get(f"/api/orders/{order_id}")
    response.raise_for_status()
    return response.json()


def create_order(
    client: APIClient,
    *,
    user_id: str,
    total_amount: float,
    status: str,
) -> dict[str, Any]:
    response = client.post(
        "/api/orders",
        json={
            "user_id": user_id,
            "total_amount": total_amount,
            "status": status,
        },
    )
    response.raise_for_status()
    return response.json()


def update_order(
    client: APIClient,
    order_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    response = client.put(f"/api/orders/{order_id}", json=payload)
    response.raise_for_status()
    return response.json()


def delete_order(client: APIClient, order_id: str) -> None:
    response = client.delete(f"/api/orders/{order_id}")
    response.raise_for_status()