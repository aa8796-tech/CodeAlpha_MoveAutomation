from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import StrEnum, auto

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

# =========================
# UI Components
# =========================
# --   Menu Component    --
@dataclass
class MenuOption:
    """
    Represents a selectable menu option.
    """

    label: str
    action: Callable[[], None]


@dataclass
class Menu:
    """
    Represents a terminal menu component.
    """

    title: str
    options: Sequence[MenuOption]


def display_menu(menu: Menu) -> None:
    """
    Render a menu component to the terminal.

    Args:
        menu:
            The menu instance to display.
    """

    display_header(menu.title)

    max_digits = len(str(len(menu.options)))

    for index, option in enumerate(menu.options, start=1):
        print(
            f"{index:0{max_digits}d}. "
            f"{option.label}"
        )


# =========================
# Input Handling
# =========================

def prompt_menu_selection(menu: Menu) -> MenuOption:
    """
    Prompt the user to select a menu option.

    Args:
        menu:
            The menu instance to interact with.

    Returns:
        MenuOption:
            The selected menu option.
    """

    while True:
        try:
            choice = int(
                input("\nEnter your choice: ")
            )

            if 1 <= choice <= len(menu.options):
                return menu.options[choice - 1]

            display_message("Choice out of range.", MessageType.WARNING)

        except ValueError:
            display_message("Enter a valid number.", MessageType.WARNING)

