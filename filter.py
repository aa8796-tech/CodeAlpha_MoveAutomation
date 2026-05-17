from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# =========================
# Base Filter
# =========================

class FileFilter(ABC):

    @abstractmethod
    def matches(self, file: Path) -> bool:
        pass

    def apply(self, files: Iterable[Path]) -> list[Path]:
        return [file for file in files if self.matches(file)]

# =========================
# Extension Filter (e.g. jpg, etc.)
# =========================
@dataclass(frozen=True)
class ExtensionFileFilter(FileFilter):
    extensions: frozenset[str]

    def matches(self, file: Path) -> bool:
        return file.suffix.lower() in self.extensions
