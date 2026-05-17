import shutil
from pathlib import Path

def execute(self, file: Path) -> None:
    """
    Moves a file to the destination directory.

    Args:
        file (Path):
            The file to be moved.

    Raises:
        FileNotFoundError:
            If the file does not exist.
        OSError:
            If the move operation fails.
    """

    if not self.destination.exists():
        self.destination.mkdir(parents=True, exist_ok=True)

    if not file.exists():
        raise FileNotFoundError(f"File not found: {file}")

    target_path = self.destination / file.name

    shutil.move(str(file), str(target_path))
