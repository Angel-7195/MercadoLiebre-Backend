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
    *,
    seller_id: str,
    category_id: str,
    name: str,
    description: str | None = None,
    brand: str | None = None,
    price: float | None = None,
    stock: int | None = None,
    status: str | None = None,
    image_url: str | None = None,
) -> dict[str, Any]:
    r = client.post(
        "/api/products",
        json={
            "seller_id": seller_id,
            "category_id": category_id,
            "name": name,
            "description": description,
            "brand": brand,
            "price": price,
            "stock": stock,
            "status": status,
            "image_url": image_url,
        },
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