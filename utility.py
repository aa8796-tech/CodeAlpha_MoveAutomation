import os
import shutil

# =========================
# Terminal Utilities
# =========================
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def pause() -> None:
    input("Press Enter to continue...")

def get_terminal_width() -> int:
    return shutil.get_terminal_size((80, 20)).columns
