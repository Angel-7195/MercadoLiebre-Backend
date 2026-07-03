import os
from getpass import getpass

from dotenv import load_dotenv
from httpx import HTTPStatusError
from rich.console import Console

from app.crud.auth import login
from app.crud.http_client import APIClient
from app.crud.menu_users import users_menu
from app.crud.menu_sellers import sellers_menu
from app.utils.cli_utils import clear_screen, pause

console = Console()

def authenticate(client: APIClient) -> bool:
    while True:
        clear_screen()
        console.print("=== LOGIN API (JWT) ===\n")
        email = input("Email: ").strip()
        password = getpass("Password: ")

        try:
            token_data = login(client, email=email, password=password)
            client.set_bearer_token(token_data["access_token"])
            console.print("\nAutentication successfull.\n")
            pause()
            return True
        except HTTPStatusError as exc:
            console.print(
                f"\nInvalid Credetials (HTTP {exc.response.status_code}).\n"
            )
            retry = input("Try again? (y/n): ").strip().lower()
            if retry == "n":
                return False

def main() -> None:
    load_dotenv()
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

    client = APIClient(base_url)
    try:
        if not authenticate(client):
            return

        while True:
            clear_screen()
            console.print("=== MAIN MENU ===\n")
            console.print("1. Sellers")
            console.print("2. Categories")
            console.print("3. Products")
            console.print("4. Shopping Cart")
            console.print("5. Users")
            console.print("6. Purchase Details")
            console.print("0. Exit\n")
            console.print("---------------------\n")

            op = input("Select an option: ").strip()

            if op == "0":
                return
            elif op == "1":
                sellers_menu(client)
            elif op == "2":
                pass
            elif op == "3":
                pass
            elif op == "4":
                pass
            elif op == "5":
                users_menu(client)
            elif op == "6":
                pass

    finally:
        client.close()


if __name__ == "__main__":
    main()
