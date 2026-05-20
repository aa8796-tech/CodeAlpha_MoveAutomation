from typing import Iterable
import os


def iter_files(directory: str) -> Iterable[str]:
    """
    Lazily iterate over all files within a directory.

    Only regular files are yielded. Subdirectories and other
    non-file entries are ignored.

    Args:
        directory:
            Path to the directory to scan.

    Yields:
        str:
            Absolute or relative file paths contained in the
            specified directory.

    Raises:
        FileNotFoundError:
            If the specified directory does not exist.

        NotADirectoryError:
            If the provided path is not a directory.

        PermissionError:
            If the program lacks permission to access
            the directory.
    """

    if not os.path.exists(directory):
        raise FileNotFoundError(
            f"Directory does not exist: {directory}"
        )

    if not os.path.isdir(directory):
        raise NotADirectoryError(
            f"Path is not a directory: {directory}"
        )

    for entry in os.scandir(directory):
        if entry.is_file():
            yield entry.path
