from __future__ import annotations

from typing import Any

from app.crud.http_client import APIClient


def list_categories(client: APIClient) -> list[dict[str, Any]]:
    r = client.get("/api/categories")
    r.raise_for_status()
    return r.json()


def get_category(client: APIClient, category_id: str) -> dict[str, Any]:
    r = client.get(f"/api/categories/{category_id}")
    r.raise_for_status()
    return r.json()


def create_category(
    client: APIClient,
    *,
    name: str,
    description: str | None = None,
) -> dict[str, Any]:
    data = {
        "name": name,
        "description": description,
    }

    r = client.post("/api/categories", json=data)
    r.raise_for_status()
    return r.json()


def update_category(
    client: APIClient,
    category_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    r = client.put(f"/api/categories/{category_id}", json=payload)
    r.raise_for_status()
    return r.json()


def delete_category(client: APIClient, category_id: str) -> None:
    r = client.delete(f"/api/categories/{category_id}")
    r.raise_for_status()