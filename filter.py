from abc import ABC, abstractmethod
import os
from typing import Iterable

class FileFilter(ABC):

    @abstractmethod
    def matches(self, file_path: str) -> bool:
        """
        Determine whether a file satisfies the filter criteria.

        Args:
            file_path: The file path to evaluate.

        Returns:
            bool: True if the file matches the filter condition,
            otherwise False.
        """
        pass

    def apply(self, file_paths: Iterable[str]) -> Iterable[str]:
        """
        Lazily apply the filter to an iterable collection of files.

        Args:
            file_paths: An iterable sequence of file paths.

        Returns:
            Iterable[str]:
                A lazy iterable yielding only file paths that satisfy
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
                {e.g. 'txt', '.png', 'jpg', 'PNG'}.
        """

        # Normalize extensions to lowercase and remove any
        # leading dots to ensure consistent comparisons.
        self.extensions = frozenset(
            ext.lower().lstrip('.')
            for ext in extensions
        )
	
    def matches(self, file_path: str) -> bool:
        """
        Check whether the file extension matches
        the configured extension set.

        Args:
            file_path: The file path to evaluate.

        Returns:
            bool:
                True if the file extension is included in the
                configured extensions, or if no extensions
                were specified, otherwise Flase.
        """

        if not self.extensions:
            return True
            
        
        file_extension = os.path.splitext(file_path)[1].lstrip('.')

        return file_extension in self.extensions
