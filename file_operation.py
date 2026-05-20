import shutil
from pathlib import Path

# Explicit type alias representing supported file path inputs.
# Accepts both raw string paths and pathlib.Path objects.
type FilePath = FolderPath = str | Path


def move_file(file: FilePath, destination: FilePath) -> None:
    """
    Moves a file to the destination directory.

    Args:
        file (FilePath):
            The file to be moved.
        destination (FolderPath):
            Destination for file transfer

    Raises:
        FileNotFoundError:
            If the file does not exist.
        OSError:
            If the move operation fails.
    """
    file = Path(file)
    destination = Path(destination)
    if not destination.exists():
        destination.mkdir(parents=True, exist_ok=True)

    if not file.exists():
        raise FileNotFoundError(f"File not found: {file}")

    target_path = destination / file.name

    shutil.move(str(file), str(target_path))
