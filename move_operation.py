import os
import shutil


def move_file(file_path: str, destination: str) -> None:
    """
    Move a file to the specified destination directory.

    The destination directory is created automatically
    if it does not already exist.

    Args:
        file_path:
            Absolute or relative path to the source file.

        destination:
            Target directory where the file will be moved.

    Raises:
        FileNotFoundError:
            If the source file does not exist.

        shutil.Error:
            If the move operation fails.

        PermissionError:
            If the program lacks the required filesystem permissions.
    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"File does not exist: {file_path}"
        )

    os.makedirs(destination, exist_ok=True)

    shutil.move(file_path, destination)
