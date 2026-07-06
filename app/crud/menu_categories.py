from __future__ import annotations

from typing import Any

import httpx
from rich.console import Console

from app.crud.categories import (
    create_category,
    delete_category,
    get_category,
    list_categories,
    update_category,
)

from app.crud.http_client import APIClient
from app.utils.cli_utils import clear_screen, pause, print_table
from app.utils.menu_utils import pick_from_list

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

def categories_menu(client: APIClient) -> None:
    payload: dict[str, Any]

    while True:

        clear_screen()

        console.print("=== CATEGORIES ===\n")
        console.print("1. List Categories")
        console.print("2. Get Category")
        console.print("3. Create Category")
        console.print("4. Update Category")
        console.print("5. Delete Category")
        console.print("0. Back to Main Menu")
        console.print("--------------------\n")

        op = input("Choose an option: ").strip()

        try:
            if op == "0":
                return
            elif op == "1":

                rows = list_categories(client)

                print_table(
                    rows,
                    columns={
                        "name": "Category Name",
                        "description": "Description",
                        "id": "ID",
                        "created_at": "Created At",
                    },
                    title="Categories",
                    empty_message="No categories found.",
                )

                pause()

            elif op == "2":

                rows = list_categories(client)

                if not rows:
                    console.print("No categories found. Please create a category first.")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select a category",
                    display=lambda c: c['name'],
                )

                if not picked:
                    continue

                category = get_category(client, picked['id'])

                print_table(
                    [category],
                    columns={
                        "name": "Category Name",
                        "description": "Description",
                        "id": "ID",
                        "created_at": "Created At",
                    },
                    title="Category Details",
                )

                pause()

            elif op == "3":

                clear_screen()
                console.print("=== CREATE CATEGORY ===\n")

                name = input("Enter category name: ").strip()
                description = input("Description: ").strip()

                payload = {
                    "name": name,
                    "description": description,
                }

                created = create_category(client, payload)
                console.print(
                    f"\nCategory created: {created['name']} ({created['id']})\n"
                )

                pause()

            elif op == "4":
                rows = list_categories(client)
                if not rows:
                    console.print("No categories found.")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select a category to update",
                    display=lambda c: c['name'],
                )
                if not picked:
                    continue

                current = get_category(client, picked["id"])
                clear_screen()
                console.print("=== UPDATE CATEGORY ===\n")
                console.print("Leave empty to keep the current value\n")

                name = input(f"Name: [{current.get('name')}]: ").strip()
                description = input(f"Description: [{current.get('description')}]: ").strip()

                payload: dict[str, Any] = {}
                if name:
                    payload["name"] = name
                if description:
                    payload["description"] = description

                if not payload:
                    console.print("\nNo changes to update\n")
                    pause()
                    continue

                updated = update_category(client, picked["id"], payload)
                console.print(
                    f"\nCategory updated: {updated['name']} ({updated['id']})\n"
                )
                pause()

            elif op == "5":
                rows = list_categories(client)

                if not rows:
                    console.print("No categories found.")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title = "Select the category to delete",
                    display=lambda c: c['name'],
                )

                if not picked:
                    continue

                confirm = (
                    input(
                        f"Delete Category '{picked['name']}? (y/N): "
                    )
                    .strip()
                    .lower()
                )

                if confirm != "y":
                    continue

                delete_category(client, picked["id"])

                console.print("\nCategory deleted successfully\n")

                pause()

            else:
                console.print("Invalid option. Please try again.")
                pause()
        except Exception as exc:
            _handle_http_error(exc)
            pause()