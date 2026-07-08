from __future__ import annotations

from typing import Any

import httpx
from rich.console import Console

from app.crud.shopping import(
    create_shopping,
    delete_shopping,
    get_shopping,
    list_shopping,
    update_shopping,
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

def shopping_menu(client: APIClient) -> None:
    payload: dict[str, Any]

    while True:

        clear_screen()
        console.print("=== MENU SHOPPING CART ===\n")
        console.print("1. List Shopping")
        console.print("2. Get Shopping")
        console.print("3. Create Shopping")
        console.print("4. Update Shopping")
        console.print("5. Delete Shopping")
        console.print("0. Back to Main Menu")
        console.print("---------------------\n")

        op = input("Choose an option: ").strip()

        try:
            if op == "0":
                return
            elif op == "1":
                
                rows = list_shopping(client)

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
                        "user_id": "User",
                        "total_amount": "Total amount",
                        "status": "Status",
                        "created_at": "Created at",
                    },
                    title="Shopping Carts",
                    empty_message="No shopping carts found",
                )

                pause()
            elif op == "2":

                rows = list_shopping(client)

                if not rows:
                    console.print("No shopping carts found.")
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
                    title="Select a Shopping cart:",
                    display=lambda s: (
                        f"{users_map.get(s['user_id'], 'Unknown')} | {s['status']}"
                    ),
                )

                if not picked:
                    continue

                shopping = get_shopping(client, picked["id"])

                # Agregar el nombre del usuario al registro
                shopping["user_name"] = users_map.get(
                    shopping["user_id"],
                    "Unknown"
                )

                print_table(
                    [shopping],
                    columns={
                        "user_name": "User",
                        "total_amount": "Total Amount",
                        "status": "Status",
                        "created_at": "Created At",
                    },
                    title="Shopping Cart",
                    empty_message="No shopping cart found.",
                )

                pause()

            elif op == "3":
                clear_screen()
                console.print("=== Create Shopping Cart===")

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

                total_amount = input("Total Amount: ").strip() or "PENDING"
                status = input("Status [PENDING]: ").strip().upper()

                created = create_shopping(
                    client,
                    user_id=user_id,
                    total_amount=total_amount,
                    status=status,
                )

                console.print(
                    f"\nShopping cart created successfully: {created['total_amount']} ({created['id']})\n"
                )

                pause()

            elif op == "4":

                rows = list_shopping(client)

                if not rows:
                    console.print("No shopping carts found")
                    pause()
                    continue

                users = list_users(client)

                users_map = {
                    u["id"]: u["full_name"]
                    for u in users
                }
                
                picked = pick_from_list(
                    rows,
                    title="Select the shopping to update:",
                    display=lambda s: (
                        f"{users_map.get(s['user_id'], 'Unknown')} | {s['status']}"
                    ),
                )

                if not picked:
                    continue

                current = get_shopping(client, picked["id"])

                clear_screen()
                console.print("=== Update Shopping cart ===\n")
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

                updated = update_shopping(
                    client,
                    picked["id"],
                    payload,
                )

                console.print(
                    f"\nShopping cart updated {updated['total_amount']} ({updated['id']})\n"
                )

                pause()
            elif op == "5":

                rows = list_shopping(client)

                if not rows:
                    console.print("No shopping cart found")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the shopping to delete",
                    display=lambda s: (
                        f"{s['total_amount']} | {s['status']}"
                    )
                )

                if not picked:
                    continue

                confirm = (
                    input(
                        f"Delete shopping '{picked['total_amount']}'? (y/N): "
                    )
                    .strip()
                    .lower()
                )

                if confirm != "y":
                    continue

                delete_shopping(client, picked["id"])

                console.print("\nShopping deleted succesfully")

                pause()

            else:
                console.print("Invalid option. Please try again")
                pause()
        except Exception as exc:
            _handle_http_error(exc)
            pause()