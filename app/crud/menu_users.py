from __future__ import annotations

from typing import Any
from getpass import getpass

import httpx
from rich.console import Console

from app.crud.http_client import APIClient
from app.crud.users import (
    create_user,
    delete_user,
    get_user,
    list_users,
    update_user,
)
from app.utils.cli_utils import clear_screen, pause, print_table
from app.utils.menu_utils import pick_from_list

console = Console()

USER_ROLES = ["CLIENT", "ADMIN"]


def _handle_http_error(exc: Exception) -> None:
    if isinstance(exc, httpx.HTTPStatusError):
        try:
            data = exc.response.json()

            if "error" in data:
                detail = data["error"]["message"]

                if data["error"].get("details"):
                    detail += f"\n{data['error']['details']}"

            else:
                detail = data.get("detail", exc.response.text)

        except Exception:
            detail = exc.response.text

        console.print(f"\n[red]HTTP {exc.response.status_code}[/red]: {detail}\n")
    else:
        console.print(f"\n[red]Error[/red]: {exc}\n")



def _pick_role(default: str = "CLIENT") -> str:
    console.print("\nRol:")
    for idx, r in enumerate(USER_ROLES, start=1):
        console.print(f"{idx}) {r}")
    console.print("0) Cancel")

    while True:
        raw = input(f"Option [{default}]: ").strip()
        if raw == "":
            return default
        if raw == "0":
            raise KeyboardInterrupt

        # permitir por número
        if raw.isdigit():
            i = int(raw)
            if 1 <= i <= len(USER_ROLES):
                return USER_ROLES[i - 1]

        # permitir escribir el texto
        up = raw.upper()
        if up in USER_ROLES:
            return up

        console.print("Invalid Option.")


def users_menu(client: APIClient) -> None:
    while True:
        clear_screen()
        console.print("=== USERS ===\n")
        console.print("1) List Users")
        console.print("2) View User")
        console.print("3) Create User")
        console.print("4) Update User")
        console.print("5) Delete User")
        console.print("0) Back to Main Menu")
        console.print("----------------------")

        op = input("Option: ").strip()

        try:
            if op == "0":
                return

            if op == "1":
                rows = list_users(client)
                print_table(
                    rows,
                    columns={
                        "full_name": "Name",
                        "email": "Email",
                        "role": "Rol",
                        "id": "ID",
                        "created_at": "Created At",
                    },
                    title="Users",
                    empty_message="No users found.",
                )
                pause()

            elif op == "2":
                rows = list_users(client)
                if not rows:
                    console.print("No users found.")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the user:",
                    display=lambda u: f"{u['full_name']} | {u['email']} | {u['role']}",
                )
                if not picked:
                    continue

                u = get_user(client, picked["id"])
                print_table(
                    [u],
                    columns={
                        "full_name": "Name",
                        "email": "Email",
                        "role": "Rol",
                        "id": "ID",
                        "created_at": "Created At",
                    },
                    title="Users",
                )
                pause()

            elif op == "3":
                clear_screen()
                console.print("=== Create User ===\n")
                email = input("Email: ").strip()
                full_name = input("Full Name: ").strip()

                 # La contraseña no se muestra mientras se escribe.

                password = getpass("Password: ")

                try:
                    role = _pick_role(default="CLIENT")
                except KeyboardInterrupt:
                    continue

                payload: dict[str, Any] = {
                    "email": email,
                    "full_name": full_name,
                    "password": password,
                    "role": role,
                }
                created = create_user(client, payload)
                console.print(
                    f"\nUser created: {created['full_name']} ({created['id']})\n"
                )
                pause()

            elif op == "4":
                rows = list_users(client)
                if not rows:
                    console.print("No users found.")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the user to update:",
                    display=lambda u: f"{u['full_name']} | {u['email']} | {u['role']}",
                )
                if not picked:
                    continue

                current = get_user(client, picked["id"])
                clear_screen()
                console.print("=== Update User ===\n")
                console.print("Leave empty to keep the current value.\n")

                email = input(f"Email [{current.get('email')}]: ").strip()
                full_name = input(
                    f"Full Name [{current.get('full_name')}]: "
                ).strip()
                password = getpass(
                    "New Password (leave blank to keep current): "
                )

                change_role = input("Change role? (y/N): ").strip().lower()
                role_value: str | None = None
                if change_role == "y":
                    try:
                        role_value = _pick_role(default=current.get("role") or "CLIENT")
                    except KeyboardInterrupt:
                        role_value = None

                payload: dict[str, Any] = {}
                if email:
                    payload["email"] = email
                if full_name:
                    payload["full_name"] = full_name
                if role_value is not None:
                    payload["role"] = role_value
                if password:
                    payload["password"] = password

                if not payload:
                    console.print("\nNo changes to update.\n")
                    pause()
                    continue

                updated = update_user(client, picked["id"], payload)
                console.print(
                    f"\nUser updated: {updated['full_name']} ({updated['id']})\n"
                )
                pause()

            elif op == "5":
                rows = list_users(client)
                if not rows:
                    console.print("No users found.")
                    pause()
                    continue

                picked = pick_from_list(
                    rows,
                    title="Select the user to delete:",
                    display=lambda u: f"{u['full_name']} | {u['email']} | {u['role']}",
                )
                if not picked:
                    continue

                confirm = (
                    input(
                        f"Delete {picked.get('full_name')} ({picked.get('email')})? (y/N): "
                    )
                    .strip()
                    .lower()
                )
                if confirm != "y":
                    continue

                delete_user(client, picked["id"])
                console.print("\nUser deleted.\n")
                pause()

            else:
                console.print("Invalid option.")
                pause()

        except Exception as exc:
            _handle_http_error(exc)
            pause()
