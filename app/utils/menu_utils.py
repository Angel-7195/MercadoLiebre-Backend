from __future__ import annotations

from typing import Any

from rich.console import Console

console = Console()

def pick_from_list(
        items: list[dict[str, Any]],
        *,
        title: str,
        display,
) -> dict[str, Any] | None:
    
    if not items:
        console.print("There are no items to select.")
        return None
    
    console.print(f"=== {title} ===\n")

    for idx, item in enumerate(items, start=1):
        console.print(f"{idx}) {display(item)}")

    console.print("0) Cancel")

    while True:
        option = input("Option:").strip()

        if option == "0":
            return None
        
        if option.isdigit():
            index = int(option)

            if 1 <= index <= len(items):
                return items[index - 1]
            
        console.print("Invalid option, please try again.")