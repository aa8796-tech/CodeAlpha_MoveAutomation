# =========================
# Terminal Utilities
# =========================
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def pause() -> Nonw:
    input("Press Enter to continue...")
