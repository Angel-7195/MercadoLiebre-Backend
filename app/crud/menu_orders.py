from __future__ import annotations

from typing import Any

import httpx
from rich.console import Console

from app.crud.orders import(
    create_order,
    delete_order,
    get_order,
    list_orders,
    update_order,
)

from app.crud.http_client import APIClient
from app.utils.cli_utils import clear_screen, pause, print_table
from app.utils.menu_utils import pick_from_list
from app.crud.users import list_users

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

def orders_menu(client: APIClient) -> None:
    payload: dict[str, Any]

    while True:

        clear_screen()
        console.print("=== MENU ORDERS ===\n")
        console.print("1. List Orders")
        console.print("2. Get Order")
        console.print("3. Create Order")
        console.print("4. Update Order")
        console.print("5. Delete Order")
        console.print("0. Back to Main Menu")
        console.print("---------------------\n")

        op = input("Choose an option: ").strip()

        try:
            if op == "0":
                return
            elif op == "1":
                
                rows = list_orders(client)

                users = list_users(client)

                users_map = {
                    u["id"]: u["full_name"]
                    for u in users
                }

                for row in rows:
                    row["user_name"] = users_map.get(row["user_id"], "Unknown")

                print_table(
                    rows,
                    columns={
                        "user_name": "User",
                        "total_amount": "Total Amount",
                        "status": "Status",
                        "created_at": "Created at",
                    },
                    title="Orders",
                    empty_message="No orders found",
                )

                pause()
            elif op == "2":

                rows = list_orders(client)

                if not rows:
                    console.print("No orders found.")
                    pause()
                    continue

                # Obtener todos los usuarios
                users = list_users(client)

                # Crear un diccionario: id -> nombre
                users_map = {
                    u["id"]: u["full_name"]
                    for u in users
                }

                picked = pick_from_list(
                    rows,
                    title="Select an Order:",
                    display=lambda s: (
                        f"{users_map.get(s['user_id'], 'Unknown')} | {s['status']}"
                    ),
                )

                if not picked:
                    continue

                order = get_order(client, picked["id"])

                # Agregar el nombre del usuario al registro
                order["user_name"] = users_map.get(
                    order["user_id"],
                    "Unknown"
                )

                print_table(
                    [order],
                    columns={
                        "user_name": "User",
                        "total_amount": "Total Amount",
                        "status": "Status",
                        "created_at": "Created At",
                    },
                    title="Orders",
                    empty_message="No orders found.",
                )

                pause()

            elif op == "3":
                clear_screen()
                console.print("=== Create Order ===")

                users = list_users(client)

                if not users:
                    console.print("No users found. please create a user first")
                    pause()
                    continue

                picked_user = pick_from_list(
                    users,
                    title="Select the user:",
                    display=lambda u: (
                        f"{u['full_name']} | {u['email']} | {u['role']}"
                    ),
                )

                if not picked_user:
                    continue

                user_id = picked_user["id"]

                console.print(f"\nSelected user: {picked_user['full_name']}\n")

                total_amount = input("Total Amount [0]: ").strip() or "0"
                status = input("Status [PENDING]: ").strip().upper() or "PENDING"

                created = create_order(
                    client,
                    user_id=user_id,
                    total_amount=total_amount,
                    status=status,
                )

                console.print(
                    f"\nOrder created successfully: {created['total_amount']} ({created['id']})\n"
                )

                pause()

            elif op == "4":

                rows = list_orders(client)

                if not rows:
                    console.print("No orders found")
                    pause()
                    continue

                users = list_users(client)

                users_map = {
                    u["id"]: u["full_name"]
                    for u in users
                }
                
                picked = pick_from_list(
                    rows,
                    title="Select the order to update:",
                    display=lambda s: (
                        f"{users_map.get(s['user_id'], 'Unknown')} | {s['status']}"
                    ),
                )

                if not picked:
                    continue

                current = get_order(client, picked["id"])

                clear_screen()
                console.print("=== Update Order ===\n")
                console.print("Leave empty to keep current value.\n")

                total_amount = input(
                    f"total Amount [{current.get('total_amount')}]: "
                ).strip()
                status = input(
                    f"status [{current.get('status')}]: "
                ).strip()

                payload: dict[str, Any] = {}

                if total_amount:
                    payload["total_amount"] = total_amount
                if status:
                    payload["status"] = status.upper()

                if not payload:
                    console.print("\nNo changes to update\n")
                    pause()
                    continue

                updated = update_order(
                    client,
                    picked["id"],
                    payload,
                )

                console.print(
                    f"\nOrder updated {updated['total_amount']} ({updated['id']})\n"
                )

                pause()
            elif op == "5":

                rows = list_orders(client)

                if not rows:
                    console.print("No order found")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the order to delete",
                    display=lambda s: (
                        f"{s['total_amount']} | {s['status']}"
                    )
                )

                if not picked:
                    continue

                confirm = (
                    input(
                        f"Delete order '{picked['total_amount']}'? (y/N): "
                    )
                    .strip()
                    .lower()
                )

                if confirm != "y":
                    continue

                delete_order(client, picked["id"])

                console.print("\nOrder deleted successfully")

                pause()

            else:
                console.print("Invalid option. Please try again")
                pause()
        except Exception as exc:
            _handle_http_error(exc)
            pause()