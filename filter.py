from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

# Explicit type alias representing supported file path inputs.
# Accepts both raw string paths and pathlib.Path objects.
type FilePath = str | Path

class FileFilter(ABC):

    @abstractmethod
    def matches(self, file: FilePath) -> bool:
        """
        Determine whether a file satisfies the filter criteria.

        Args:
            file: The file path to evaluate.

        Returns:
            bool: True if the file matches the filter condition,
            otherwise False.
        """
        pass

    def apply(self, files: Iterable[FilePath]) -> Iterable[FilePath]:
        """
        Lazily apply the filter to an iterable collection of files.

        Args:
            files: An iterable sequence of file paths.

        Returns:
            Iterable[FilePath]:
                A lazy iterable yielding only files that satisfy
                the filter criteria.
        """
        return (f for f in files if self.matches(f))


class ExtensionFileFilter(FileFilter):
    """
    Filter files based on their file extensions.

    Extensions are normalized internally to ensure
    case-insensitive matching and consistent formatting.
    """

    def __init__(self, extensions: frozenset[str]):
        """
        Initialize the extension filter.

        Args:
            extensions:
                frozenset of file extensions
                {e.g. 'txt', '.png', 'jpg'}.
        """

        # Normalize extensions to lowercase and remove any
        # leading dots to ensure consistent comparisons.
        self.extensions = frozenset(
            ext.lower().lstrip('.')
            for ext in extensions
        )
	
    def matches(self, file: FilePath) -> bool:
        """
        Check whether the file extension matches
        the configured extension set.

        Args:
            file: The file path to evaluate.

        Returns:
            bool:
                True if the file extension is included in the
                configured extensions, or if no extensions
                were specified.
        """

        if not self.extensions:
            return True
            
        # Convert input to a Path object to ensure a unified
        # and reliable extension extraction process.
        file_extension = Path(file).suffix.lower().lstrip('.')

        return file_extension in self.extensions
