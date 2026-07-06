from __future__ import annotations

from typing import Any

from app.crud.http_client import APIClient


def list_products(client: APIClient) -> list[dict[str, Any]]:
    r = client.get("/api/products")
    r.raise_for_status()
    return r.json()


def get_product(client: APIClient, product_id: str) -> dict[str, Any]:
    r = client.get(f"/api/products/{product_id}")
    r.raise_for_status()
    return r.json()


def create_product(
    client: APIClient,
    payload: dict[str, Any],
) -> dict[str, Any]:

    r = client.post(
        "/api/products",
        json=payload,
    )

    r.raise_for_status()

    return r.json()


def update_product(
    client: APIClient,
    product_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    r = client.put(f"/api/products/{product_id}", json=payload)
    r.raise_for_status()
    return r.json()


def delete_product(client: APIClient, product_id: str) -> None:
    r = client.delete(f"/api/products/{product_id}")
    r.raise_for_status()