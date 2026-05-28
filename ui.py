"""Terminal user interface components and display utilities.

This module provides immutable data models for menu construction and 
functions for rendering standardized, validated terminal interactions.
"""

from collections.abc import Callable, Sequence, Iterable
from dataclasses import dataclass
from enum import StrEnum, auto

from utility import get_terminal_width
from validation import validate, ValidationResult, is_in_range, is_not_blank, Validator

terminal_width: int = get_terminal_width()
BORDER_CHAR: str = "="
BORDER_LENGTH: int = terminal_width // 2


class MessageType(StrEnum):
    """Semantic classifications for terminal output messages."""
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    NOTE = auto()
    ERROR = auto()


MESSAGE_PREFIXES: dict[MessageType, str] = {
    MessageType.INFO: "",
    MessageType.SUCCESS: "[✔] SUCCESS: ",
    MessageType.WARNING: "[⚠️] WARNING: ",
    MessageType.NOTE: "[!] NOTE: ",
    MessageType.ERROR: "[✖] ERROR: "
}


def display_divider() -> None:
    """Render a centered horizontal divider line to stdout."""
    print((BORDER_CHAR * BORDER_LENGTH).center(terminal_width))


def display_message(message: str, message_type: MessageType = MessageType.INFO) -> None:
    """Print a contextualized message to stdout.

    Args:
        message (str): The payload text to display.
        message_type (MessageType): The classification defining the message prefix.
    """
    prefix = MESSAGE_PREFIXES.get(message_type, "")
    print(f"{prefix}{message}")


def display_header(title: str) -> None:
    """Render a formatted section header.

    Args:
        title (str): The header text to display.
    """
    display_divider()
    print(f"{title:^{terminal_width}}")
    display_divider()


@dataclass(frozen=True)
class MenuItem:
    """Immutable representation of a selectable menu option.

    Attributes:
        label (str): The display text for the option.
        action (Callable[[], None] | None): Optional callback triggered upon selection.
    """
    label: str
    action: Callable[[], None] | None = None


@dataclass(frozen=True)
class Menu:
    """Immutable configuration for a terminal menu interface.

    Attributes:
        title (str): The primary heading of the menu.
        options (Sequence[MenuItem]): The available selection items.
    """
    title: str
    options: Sequence[MenuItem]

    def __post_init__(self) -> None:
        """Validate instance integrity upon initialization."""
        if not self.options:
            raise ValueError(f"Menu '{self.title}' requires at least one MenuItem.")


def display_menu(menu: Menu) -> None:
    """Render a structured menu with dynamically padded indexing.

    Args:
        menu (Menu): The menu configuration object to display.
    """
    print(f"{menu.title}:")
    max_digits = len(str(len(menu.options)))

    for index, option in enumerate(menu.options, start=1):
        print(f"  {index:0{max_digits}d}. {option.label}")

# =============================
# Input Helper with Validation
# =============================
def get_validated_input(prompt_text: str, validators: Iterable[Validator]) -> str:
    """Prompt the user for input and run it through the validation engine.

    Loops continuously until the input satisfies all specified validation rules.
    """
    while True:
        user_input = input(prompt_text).strip()
        errors = validate(user_input, validators)
        
        if not errors:
            return user_input
            
        # Display the validation error messages safely
        for error in errors:
            display_message(error.message, MessageType.ERROR)

def prompt_menu_selection(menu: Menu) -> MenuItem:
    """Prompt and validate user selection against the provided menu boundaries.

    Args:
        menu (Menu): The active menu context.

    Returns:
        MenuItem: The verified menu option selected by the user.
    """
    options_count = len(menu.options)
    
    menu_validators = [
        is_not_blank,
        lambda value: ValidationResult(
            is_valid=value.isdigit(), 
            message="Please enter a positive integer numerical value."
        ),
        is_in_range(
            min_val=1, 
            max_val=options_count, 
            custom_error=f"Choice out of range. Enter a number between 1 and {options_count}."
        )
    ]
    
    choice_str = get_validated_input("\nEnter your choice: ", menu_validators)
    return menu.options[int(choice_str) - 1]
