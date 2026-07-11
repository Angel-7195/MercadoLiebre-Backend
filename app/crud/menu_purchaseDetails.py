from __future__ import annotations

from typing import Any

import httpx
from rich.console import Console

from app.crud.purchase_details import(
    create_purchase_detail,
    delete_purchase_detail,
    get_purchase_detail,
    list_purchase_details,
    update_purchase_detail,
)

from app.crud.http_client import APIClient
from app.utils.cli_utils import clear_screen, pause, print_table
from app.utils.menu_utils import pick_from_list
from app.crud.products import list_products
from app.crud.orders import list_orders

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


def purchaseDetails_menu(client: APIClient) -> None:
    payload: dict[str, Any]

    while True:

        clear_screen()
        console.print("=== PURCHASE DETAILS ===\n")
        console.print("1. List Purchases")
        console.print("2. Get Purchase")
        console.print("3. Create Purchase")
        console.print("4. Update Purchase")
        console.print("5. Delete Purchase")
        console.print("0. Back to Main Menu")
        console.print("---------------------\n")

        op = input("Choose an option: ").strip()

        try:
            if op == "0":
                return
            elif op == "1":
                
                rows = list_purchase_details(client)

                products = list_products(client)

                products_map = {
                    p["id"]: p["name"]
                    for p in products
                }

                for row in rows:
                    row["product_name"] = products_map.get(row["product_id"], "Unknown")

                orders = list_orders(client)

                orders_map = {
                    o["id"]: o["status"]
                    for o in orders
                }

                for row in rows:
                    row["order_status"] = orders_map.get(row["order_id"], "Unknown")

                print_table(
                    rows,
                    columns={
                        "quantity": "Quantity",
                        "unit_price": "Unit price",
                        "subtotal": "Subtotal",
                        "order_status": "Order status",
                        "product_name": "Product",
                        "created_at": "Created at",
                    },
                    title="Purchase Details",
                    empty_message="No purchases found"
                )

                pause()
            elif op == "2":
                
                rows = list_purchase_details(client)

                if not rows:
                    console.print("No purchases found.")
                    pause()
                    continue

                products = list_products(client)

                products_map = {
                    p["id"]: p["name"]
                    for p in products
                }

                picked = pick_from_list(
                    rows,
                    title="Select a purchase:",
                    display=lambda p: (
                        f"{products_map.get(p['product_id'], 'Unknown')}"
                    ),
                )

                if not picked:
                    continue

                purchase = get_purchase_detail(client, picked ["id"])

                purchase["product_name"] = products_map.get(
                    purchase["product_id"],
                    "Unknown"
                )

                print_table(
                    [purchase],
                    columns={
                        "quantity": "Quantity",
                        "unit_price": "Unit price",
                        "subtotal": "Subtotal",
                        "order_id": "Order status",
                        "product_name": "Product",
                        "created_at": "Created at",
                    },
                    title="Purchase Details",
                    empty_message="No purchases found"
                )

                pause()

            elif op == "3":
                
                clear_screen()
                console.print("=== Create Purchase ===\n")

                products = list_products(client)

                if not products:
                    console.print("No products found")
                    pause()
                    continue

                picked_product = pick_from_list(
                    products,
                    title="Select the product:",
                    display=lambda p: (
                        f"{p['name']} | {p['brand']} | ${p['price']}"
                    ),
                )

                if not picked_product:
                    continue

                product_id = picked_product["id"]

                console.print(f"\nSelected product: {picked_product['name']}\n")

                orders = list_orders(client)

                if not orders:
                    console.print("No orders found")
                    pause()
                    continue
                
                picked_order = pick_from_list(
                    orders,
                    title="Select the order:",
                    display=lambda o: (
                        f"{o['total_amount']} | {o['status']}"
                    ),
                )

                if not picked_order:
                    continue

                order_id = picked_order["id"]

                console.print(f"\nSelected order: ${picked_order['total_amount']} ({picked_order['status']})\n")

                quantity = int(input("Quantity: "))
                unit_price = picked_product["price"]
                subtotal = quantity * unit_price

                payload = {
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "subtotal": subtotal,
                }

                created = create_purchase_detail(client, payload)

                console.print(
                    f"\nPurchase detail created succsessfully: {created['id']}\n"
                )

                pause()

            elif op == "4":
                
                rows = list_purchase_details(client)

                if not rows:
                    console.print("No purchase details found")
                    pause()
                    continue

                products = list_products(client)
                orders = list_orders(client)

                products_map = {
                    p["id"]: p["name"]
                    for p in products
                }

                orders_map = {
                    o["id"]: o["status"]
                    for o in orders
                }

                for row in rows:
                    row["product_name"] = products_map.get(row["product_id"], "Unknown")
                    row["order_status"] = orders_map.get(row["order_id"], "Unknown")

                picked = pick_from_list(
                    rows,
                    title="Select the purchase detail to update:",
                    display=lambda p: (
                        f"{p['product_name']} | {p['order_status']}"
                    ),
                )

                if not picked:
                    continue

                current = get_purchase_detail(client, picked["id"])
                payload: dict[str, Any] = {}

                clear_screen()
                console.print("=== Update Purchase Detail ===\n")
                console.print("Leave empty to keep current value\n")

                quantity= input(
                    f"Quantity [{current.get('quantity')}]: "
                ).strip()
                unit_price= input(
                    f"Unit price [{current.get('unit_price')}]"
                ).strip()
                if quantity and unit_price:
                    subtotal = int(quantity) * float(unit_price)
                else:
                    subtotal = None

                console.print(
                    f"\nCurrent Product: {products_map.get(current['product_id'], 'Unknown')}"
                )
                change_product = input("Change Product? (y/N): ").strip().lower()

                picked_product = None

                if change_product == "y":
                    products = list_products(client)

                    picked_product = pick_from_list(
                        products,
                        title="Select the new product:",
                        display=lambda p:(
                            f"{p['name']} | {p['brand']} | ${p['price']}"
                        ),
                    )
                
                if picked_product:
                    payload["product_id"] = picked_product["id"]

                console.print(
                    f"\nCurrent Order Status: {orders_map.get(current['order_id'], 'Unknown')}"
                )
                change_order = input("Change Order? (y/N): ").strip().lower()

                picked_order = None

                if change_order == "y":
                    orders = list_orders(client)

                    picked_order = pick_from_list(
                        orders,
                        title="Select the new order:",
                        display=lambda o:(
                            f"{o['total_amount']} | {o['status']}"
                        ),
                    )

                if picked_order:
                    payload["order_id"] = picked_order["id"]
                if quantity:
                    payload["quantity"] = int(quantity)
                if unit_price:
                    payload["unit_price"] = unit_price
                if subtotal is not None:
                    payload["subtotal"] = subtotal

                if not payload:
                    console.print("\nNo changes to update.\n")
                    pause()
                    continue

                updated = update_purchase_detail(
                    client,
                    picked["id"],
                    payload,
                )

                console.print(
                    f"\nPurchase detail updated: ({updated['id']})\n"
                )

                pause()

            elif op == "5":
                
                rows = list_purchase_details(client)
                if not rows:
                    console.print("No Purchases found")
                    pause()
                    continue

                products = list_products(client)
                orders = list_orders(client)

                products_map = {
                    p["id"]: p["name"]
                    for p in products
                }

                orders_map = {
                    o["id"]: o["status"]
                    for o in orders
                }

                for row in rows:
                    row["product_name"] = products_map.get(
                        row["product_id"],
                        "Unknown"
                    )
                    row["order_status"] = orders_map.get(
                        row["order_id"],
                        "Unknown"
                    )

                picked = pick_from_list(
                    rows,
                    title="Select the Purchase detail to delete:",
                    display=lambda p: (
                        f"{p['product_name']} | {p['order_status']}"
                    ),
                )

                if not picked:
                    continue

                confirm = (
                    input(
                        f"Delete Purchase'{picked['product_name']}? (y/N): "
                    )
                    .strip()
                    .lower()
                )

                if confirm != "y":
                    continue

                delete_purchase_detail(client, picked["id"])

                console.print("\nPurchase deleted successfully")

                pause()
                
            else:
                console.print("Invalid option. Please try again")
                pause()
        except Exception as exc:
            _handle_http_error(exc)
            pause()

