# =========================
# Terminal Utilities
# =========================
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("Press Enter to continue...")
