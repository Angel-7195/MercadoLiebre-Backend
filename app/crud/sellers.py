from __future__ import annotations

from typing import Any

from app.crud.http_client import APIClient

def list_sellers(client: APIClient) -> list[dict[str, Any]]:
    r = client.get("/api/sellers")
    r.raise_for_status()
    return r.json()

def get_seller(client: APIClient, seller_id: str) -> dict[str, Any]:
    r = client.get(f"/api/sellers/{seller_id}")
    r.raise_for_status()
    return r.json()

def create_seller(
    client: APIClient,
    *,
    user_id: str,
    document_number: str,
    store_name: str,
    phone: str | None = None,
) -> dict[str, Any]:
    r = client.post("/api/sellers", json={
        "user_id": user_id,
        "document_number": document_number,
        "store_name": store_name,
        "phone": phone,
    })
    r.raise_for_status()
    return r.json()

def update_seller(
    client: APIClient,
    seller_id: str,
    payload: dict[str, Any],
    ) -> dict[str, Any]:
    r = client.put(f"/api/sellers/{seller_id}", json=payload)
    r.raise_for_status()
    return r.json()

def delete_seller(client: APIClient, seller_id: str) -> None:
    r = client.delete(f"/api/sellers/{seller_id}")
    r.raise_for_status()