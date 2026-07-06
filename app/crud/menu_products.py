from __future__ import annotations

from typing import Any

import httpx
from rich.console import Console

from app.crud.products import (
    create_product,
    delete_product,
    get_product,
    list_products,
    update_product,
)

from app.crud.http_client import APIClient
from app.utils.cli_utils import clear_screen, pause, print_table
from app.utils.menu_utils import pick_from_list
from decimal import Decimal

console = Console()

from app.crud.http_client import APIClient
from app.utils.cli_utils import clear_screen, pause, print_table
from app.utils.menu_utils import pick_from_list
from app.crud.sellers import list_sellers
from app.crud.categories import list_categories

console = Console()

def _handle_http_error(exc: Exception) -> None:
    if isinstance(exc, httpx.HTTPStatusError):
        try:
            detail = exc.response.json().get("detail")
        except Exception:
            detail = exc.response.text
        console.print(f"\n[red]HTTP {exc.response.status_code}[/red]: {detail}\n")
    else:
        console.print(f"\n[red]Error[/red]: {exc}\n")

def products_menu(client: APIClient) -> None:
    payload: dict[str, Any]

    while True:

        clear_screen()

        console.print("=== PRODUCTS ===\n")
        console.print("1. List Products")
        console.print("2. Get Products")
        console.print("3. Create Product")
        console.print("4. Update Product")
        console.print("5. Delete Product")
        console.print("0. Back to Main Menu")
        console.print("---------------------\n")

        op = input("Choose an option: ").strip()

        try:
            if op == "0":
                return
            elif op == "1":
                
                rows = list_products(client)

                print_table(
                    rows,
                    columns={
                        "name": "Product Name",
                        "description": "Product description",
                        "brand": "Brand",
                        "price": "Price",
                        "stock": "Stock",
                        "status": "Status",
                        "image_url": "Product Image",
                        "id": "ID",
                        "seller_id": "Seller ID",
                        "category_id": "Category ID",
                        "created_at": "Created At"
                    },
                    title="Products",
                    empty_message="No Products found",
                )

                pause()

            elif op == "2":
                
                rows = list_products(client)

                if not rows:
                    console.print("No Products found")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the Product:",
                    display=lambda p: (
                        f"{p['name']} | {p['brand']} | {p['image_url']}"
                    ),
                )

                if not picked:
                    continue

                product = get_product(client, picked["id"])

                print_table(
                    [product],
                    columns={
                        "name": "Product Name",
                        "description": "Product description",
                        "brand": "Brand",
                        "price": "Price",
                        "stock": "Stock",
                        "status": "Status",
                        "image_url": "Product Image",
                        "id": "ID",
                        "seller_id": "Seller ID",
                        "category_id": "Category ID",
                        "created_at": "Created At"
                    },
                    title="Product"
                )

                pause()
            elif op == "3":
                
                clear_screen()
                console.print("=== Create Product ===\n")

                sellers = list_sellers(client)

                if not sellers:
                    console.print("No sellers found")
                    pause()
                    continue

                picked_seller = pick_from_list(
                    sellers,
                    title="Select the seller:",
                    display=lambda s: (
                        f"{s['store_name']} | {s['document_number']} | {s['phone']}"
                    ),
                )

                if not picked_seller:
                    continue

                seller_id = picked_seller["id"]

                console.print(f"\nSelected seller: {picked_seller['store_name']}\n")

                categories = list_categories(client)

                if not categories:
                    console.print("No categories found")
                    pause()
                    continue

                picked_category = pick_from_list(
                    categories,
                    title="Select the category:",
                    display=lambda c: (
                        f"{c['name']}"
                    ),
                )

                if not picked_category:
                    continue

                category_id = picked_category["id"]

                console.print(f"\nSelected category: {picked_category['name']}\n")

                name = input("Product name: ").strip()
                description = input("Description: ").strip()
                brand = input("Brand: ").strip()
                price= input("Price: ").strip()
                stock = input("Stock: ").strip()
                status = input("Status [ACTIVE]: ").strip().upper()
                image_url = input("Image URL: ").strip()

                if not price or not stock:
                    console.print("\n Price and stock are required.\n")
                    pause()
                    continue

                payload = {
                    "seller_id": seller_id,
                    "category_id": category_id,
                    "name": name,
                    "description": description,
                    "brand": brand,
                    "price": float(price),
                    "stock": int(stock),
                    "status": status or "ACTIVE",
                    "image_url": image_url,
                }

                created = create_product(client, payload)

                console.print(
                    f"\nProduct created successfully: {created['name']} ({created['id']})\n"
                )

                pause()

            elif op == "4":
                
                rows = list_products(client)

                if not rows:
                    console.print("No products found.")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the product to update:",
                    display=lambda p: (
                        f"{p['name']} | {p['brand']}"
                    ),
                )

                if not picked:
                    continue

                current = get_product(client, picked["id"])

                clear_screen()
                console.print("=== Update Product ===\n")
                console.print("Leave empty to keep current value\n")

                name= input(
                    f"Name [{current.get('name')}]: "
                ).strip()
                description= input(
                    f"Description [{current.get('description')}]"
                ).strip()
                brand= input(
                    f"Brand [{current.get('brand')}]"
                ).strip()
                price= input(
                    f"Price [{current.get('price')}]"
                ).strip()
                stock= input(
                    f"Stock [{current.get('stock')}]"
                ).strip()
                status= input(
                    f"Status [{current.get('status')}]: "
                ).strip().upper()
                image_url= input(
                    f"Image url [{current.get('image_url')}]"
                ).strip()
                
                console.print(f"\nCurrent Seller ID: {current['seller_id']}")
                change_seller = input("Change seller? (y/N): ").strip().lower()

                if change_seller == "y":
                    sellers = list_sellers(client)

                    picked_seller = pick_from_list(
                        sellers,
                        title="Select the new seller:",
                        display=lambda s:(
                            f"{s['store_name']} | {s['document_number']}"
                        ),
                    )

                    if picked_seller:
                        payload["seller_id"] = picked_seller["id"]
                
                console.print(f"Current Category ID: {current['category_id']}\n")
                change_category = input("Change category? (y/N):").strip().lower()

                if change_category == "y":
                    categories = list_categories(client)

                    picked_category = pick_from_list(
                        categories,
                        title="Select the new category",
                        display=lambda c: c["name"],
                    )

                if picked_category:
                    payload["category_id"] = picked_category["id"]

                payload: dict[str, Any] = {}
                
                if name:
                    payload["name"] = name
                if description:
                    payload["description"] = description
                if brand:
                    payload["brand"] = brand
                if price:
                    payload["price"] = float(price)
                if stock:
                    payload["stock"] = int(stock)
                if status:
                    payload["status"] = status.upper()
                if image_url:
                    payload["image_url"] = image_url


                if not payload:
                    console.print("\nNo changes to update.\n")
                    pause()
                    continue

                updated = update_product(
                    client,
                    picked["id"],
                    payload,
                )

                console.print(
                    f"\nProduct updated: {updated['name']} ({updated['id']})\n"
                )

                pause()

            elif op == "5":
                
                rows = list_products(client)
                if not rows:
                    console.print("No products found")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the seller to delete",
                    display=lambda p: (
                        f"{p['name']} | {p['brand']}"
                    )
                )

                if not picked:
                    continue

                confirm = (
                    input(
                        f"Delete Product'{picked['name']}'? (y/N): "
                    )
                    .strip()
                    .lower()
                )

                if confirm != "y":
                    continue

                delete_product(client, picked["id"])

                console.print("\nProduct deleted succesfully")

                pause()

            else:
                console.print("Invalid option. Please try again")
                pause()
        except Exception as exc:
            _handle_http_error(exc)
            pause()
