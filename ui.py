from enum import StrEnum, auto
from typing import List, Optional, Type

from utility import (
    clear_screen,
    pause,
    read_input,
    convert
)

from validation import validate, Validator, ValidationResult

# =========================
# Config
# =========================
BORDER_CHAR = "="
BORDER_LENGTH = 50

# =========================
# Message Types
# =========================

class MessageType(StrEnum):
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    NOTE = auto()
    ERROR = auto()


MESSAGE_PREFIXES = {
    MessageType.INFO: "",
    MessageType.SUCCESS: "[✔] SUCCESS: ",
    MessageType.WARNING: "[⚠️] WARNING: ",
    MessageType.NOTE: "[!] NOTE: ",
    MessageType.ERROR: "[✖] ERROR: "
}


# =========================
# Display Functions
# =========================

def display_divider():
    print(BORDER_CHAR * BORDER_LENGTH)


def display_message(message: str, message_type: MessageType = MessageType.INFO):
    prefix = MESSAGE_PREFIXES.get(message_type, "")
    print(f"{prefix}{message}")


def display_header(title: str):
    display_divider()
    print(f"{title:^{BORDER_LENGTH}}")
    display_divider()


def display_menu(title: str, items: List[str], indent: int = 2):
    print(title)

    max_digits = len(str(len(items)))
    space = " " * indent

    for i, item in enumerate(items, start=1):
        print(f"{space}{i:0{max_digits}d}. {item}")


# =========================
# Input Handler
# =========================

def get_valid_input(
    prompt: str,
    validators: Optional[List[Validator]] = None,
    return_type: Optional[Type] = None
):
    while True:
        value = read_input(prompt)

        if validators:
            result = validate(value, validators)

            if not result.is_valid:
                display_message(result.message, MessageType.ERROR)
                continue

        try:
            return convert(value, return_type)
        except Exception:
            display_message("Conversion failed", MessageType.ERROR)


# =========================
# Menu Component
# =========================

def prompt_menu_selection(title: str, items: List[str]) -> int:
    if not items:
        raise ValueError("Menu cannot be empty")

    display_menu(title, items)
    display_divider()

    validators = [
        lambda x: ValidationResult(x.isdigit(), "Enter a number"),
        lambda x: ValidationResult(
            (1 <= int(x) <= len(items)) if x.isdigit() else False,
            "Choice out of range"
        )
    ]

    choice = get_valid_input("Enter your choice: ", validators)

    return int(choice)

