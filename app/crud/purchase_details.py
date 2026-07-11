from __future__ import annotations

from typing import Any

from app.crud.http_client import APIClient


def list_purchase_details(client: APIClient) -> list[dict[str, Any]]:
    response = client.get("/api/purchase_details")
    response.raise_for_status()
    return response.json()


def get_purchase_detail(
    client: APIClient,
    purchase_detail_id: str,
) -> dict[str, Any]:
    response = client.get(f"/api/purchase_details/{purchase_detail_id}")
    response.raise_for_status()
    return response.json()


def create_purchase_detail(
    client: APIClient,
    payload: dict[str, Any],
) -> dict[str, Any]:

    response = client.post(
        "/api/purchase_details",
        json=payload,
    )

    response.raise_for_status()
    return response.json()


def update_purchase_detail(
    client: APIClient,
    purchase_detail_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:

    response = client.put(
        f"/api/purchase_details/{purchase_detail_id}",
        json=payload,
    )

    response.raise_for_status()
    return response.json()


def delete_purchase_detail(
    client: APIClient,
    purchase_detail_id: str,
) -> None:

    response = client.delete(f"/api/purchase_details/{purchase_detail_id}")
    response.raise_for_status()