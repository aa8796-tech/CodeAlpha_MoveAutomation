import os
from typing import Any, Optional, Type

# =========================
# Core Utilities
# =========================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("Press Enter to continue...")

def read_input(prompt: str) -> str:
    return input(prompt).strip()

def convert(value: str, return_type: Optional[Type]) -> Any:
    if return_type is None:
        return value

    try:
        return return_type(value)
    except (ValueError, TypeError):
        return value

