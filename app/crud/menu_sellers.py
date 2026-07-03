from __future__ import annotations

from typing import Any

import httpx
from rich.console import Console

from app.crud.sellers import(
    create_seller,
    delete_seller,
    get_seller,
    list_sellers,
    update_seller,
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


def sellers_menu(client: APIClient) -> None:
    payload: dict[str, Any]
    
    while True:

        clear_screen()

        console.print("=== SELLERS ===\n")
        console.print("1) List Sellers")
        console.print("2) Get Seller by ID")
        console.print("3) Create Seller")
        console.print("4) Update Seller")
        console.print("5) Delete Seller")
        console.print("0) Back to Main Menu")
        console.print("--------------------\n")

        op = input("Choose an option: ").strip()

        try:
            if op == "0":
                return
            
            elif op == "1":

                rows = list_sellers(client)

                print_table(
                    rows,
                    columns={
                        "store_name": "Store Name",
                        "document_number": "Document Number",
                        "phone": "Phone Number",
                        "rating": "Rating",
                        "user_id": "User ID",
                        "id": "ID",
                        "created_at": "Created At",
                    },
                    title="Sellers",
                    empty_message="No sellers found.",
                )

                pause()

            elif op == "2":

                rows = list_sellers(client)

                if not rows:
                    console.print("No sellers found.")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the seller:",
                    display=lambda s: (
                        f"{s['store_name']} | {s['document_number']}"
                    ),
                )

                if not picked:
                    continue

                seller = get_seller(client, picked["id"])

                print_table(
                    [seller],
                    columns={
                        "store_name": "Store Name",
                        "document_number": "Document Number",
                        "phone": "Phone Number",
                        "rating": "Rating",
                        "user_id": "User ID",
                        "id": "ID",
                        "created_at": "Created At",
                    },
                    title="Seller Details",
                )

                pause()

            elif op == "3":

                clear_screen()
                console.print("=== Create Seller ===\n")

                users = list_users(client)
                
                # Obtener todos los usuarios registrados
                if not users:
                    console.print("No users found. Please create a user first.")
                    pause()
                    continue

                # Mostrar la lista de usuarios para seleccionar
                picked_user = pick_from_list(
                    users,
                    title="Select the user:",
                    display=lambda u: (
                        f"{u['full_name']} | {u['email']} | {u['role']}"
                    ),
                )

                # Si el usuario cancela
                if not picked_user:
                    continue

                # El UUID del usuario seleccionado será el que se envíe a la API
                user_id = picked_user["id"]

                console.print(f"\nSelected user: {picked_user['full_name']}\n")

                document_number = input("Document Number: ").strip()
                store_name = input("Store Name: ").strip()
                phone = input("Phone (optional): ").strip() or None

                created = create_seller(
                    client,
                    user_id=user_id,
                    document_number=document_number,
                    store_name=store_name,
                    phone=phone,
                )

                console.print(
                    f"\nSeller created successfully: {created['store_name']} ({created['id']})\n"
                )
                
                pause()

            elif op == "4":

                rows = list_sellers(client)

                if not rows:
                    console.print("No sellers found.")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the seller to update:",
                    display=lambda s: (
                        f"{s['store_name']} | {s['document_number']}"
                    ),
                )

                if not picked:
                    continue

                current = get_seller(client, picked["id"])

                clear_screen()
                console.print("=== Update Seller ===\n")
                console.print("Leave empty to keep current value.\n")

                document_number = input(
                    f"Document Number [{current.get('document_number')}]: "
                ).strip()

                store_name = input(
                    f"Store Name [{current.get('store_name')}]: "
                ).strip()

                phone = input(
                    f"Phone [{current.get('phone') or ''}]: "
                ).strip()

                payload: dict[str, Any] = {}

                if document_number:
                    payload["document_number"] = document_number

                if store_name:
                    payload["store_name"] = store_name

                if phone:
                    payload["phone"] = phone

                if not payload:
                    console.print("\nNo changes to update.\n")
                    pause()
                    continue

                updated = update_seller(
                    client,
                    picked["id"],
                    payload,
                )

                console.print(
                    f"\nSeller updated: {updated['store_name']} ({updated['id']})\n"
                )

                pause()

            elif op == "5":

                rows = list_sellers(client)

                if not rows:
                    console.print("No sellers found.")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the seller to delete:",
                    display=lambda s: (
                        f"{s['store_name']} | {s['document_number']}"
                    )
                )

                if not picked:
                    continue

                confirm = (
                    input(
                        f"Delete Seller'{picked['store_name']}'? (y/N): "
                    )
                    .strip()
                    .lower()
                )

                if confirm != "y":
                    continue

                delete_seller(client, picked["id"])

                console.print("\nSeller deleted successfully.\n")
                
                pause()
                
            else:
                console.print("Invalid Option, please try again")
                pause()

        except Exception as exc:
            _handle_http_error(exc)
            pause()