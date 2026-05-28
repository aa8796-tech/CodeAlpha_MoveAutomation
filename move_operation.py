"""File migration utilities utilizing structured outcome signaling.

This module defines the enumeration of possible file movement outcomes,
a structured result container, and the core safe file movement function.
"""

from dataclasses import dataclass
from enum import StrEnum, auto
import os
import shutil


class MoveStatus(StrEnum):
    """Semantic outcome codes for file movement operations."""

    SUCCESS = auto()
    CONFLICT_ALREADY_EXISTS = auto()
    PERMISSION_DENIED = auto()
    SOURCE_NOT_FOUND = auto()
    SYSTEM_ERROR = auto()


@dataclass(frozen=True)
class MoveResult:
    """Structured encapsulation of a file movement operation's outcome.

    Attributes:
        status (MoveStatus): The exact categorical result of the operation.
        message (str): Contextual error or status message, if applicable.
        destination_path (str): The final resolved path of the moved file.
    """

    status: MoveStatus
    message: str = ""
    destination_path: str = ""


def move_file(file_path: str, destination_dir: str, overwrite: bool = False) -> MoveResult:
    """Safely move a file to a destination directory with conflict pre-evaluation.

    This function inspects the source and destination paths prior to execution
    to catch predictable errors (such as missing source files or file conflicts)
    before performing the filesystem operation. System-level exceptions are
    caught and translated into structured status results.

    Args:
        file_path (str): Path to the target source file to be moved.
        destination_dir (str): Path to the target destination directory.
        overwrite (bool): If True, existing files at the target path will be
            replaced. Defaults to False.

    Returns:
        MoveResult: A structured report indicating the precise semantic outcome
            and related metadata.
    """
    if not os.path.isfile(file_path):
        return MoveResult(
            status=MoveStatus.SOURCE_NOT_FOUND,
            message="The specified source file does not exist or is inaccessible."
        )

    target_path = os.path.join(destination_dir, os.path.basename(file_path))

    if os.path.exists(target_path) and not overwrite:
        return MoveResult(
            status=MoveStatus.CONFLICT_ALREADY_EXISTS,
            message=f"A file already exists at the destination path: {target_path}",
            destination_path=target_path
        )

    try:
        os.makedirs(destination_dir, exist_ok=True)
        shutil.move(file_path, target_path)
        return MoveResult(status=MoveStatus.SUCCESS, destination_path=target_path)

    except PermissionError:
        return MoveResult(
            status=MoveStatus.PERMISSION_DENIED,
            message="The operation failed due to insufficient filesystem privileges."
        )
    except Exception as err:
        return MoveResult(status=MoveStatus.SYSTEM_ERROR, message=str(err))
