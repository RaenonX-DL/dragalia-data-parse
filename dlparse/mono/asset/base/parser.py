"""Base parser class."""
from abc import ABC, abstractmethod
from typing import Any, TextIO

__all__ = ("ParserBase",)


class ParserBase(ABC):
    """Base parser class for parsing the asset file."""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        raise RuntimeError(
            "Parser class is not allowed to be instantiated. "
            "Use the class methods or static methods directly instead."
        )

    @staticmethod
    @abstractmethod
    def parse_file(file_like: TextIO) -> Any:
        """Parse the file."""
        raise NotImplementedError()
