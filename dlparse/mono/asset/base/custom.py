"""Classes for custom assets."""
import json
from abc import ABC
from typing import Generic, TextIO, TypeVar

from dlparse.errors import AssetKeyMissingError
from .parser import ParserBase

__all__ = ("CustomParserBase",)

T = TypeVar("T")


class CustomParserBase(Generic[T], ParserBase[dict[int, T]], ABC):
    """
    Base parser class for parsing the custom asset files.

    A custom json asset file should be a list of entries.
    Each entries should have a field ``_Id`` to uniquely identifies the corresponding entry.
    """

    @staticmethod
    def get_entries_dict(file_like: TextIO, key: str = "_Id") -> dict[int, dict]:
        """
        Get a dict of data entries to be further parsed.

        The ``key`` of the return will be the value of the data with ``key``.
        This can be overridden by providing the key name.
        """
        data = json.load(file_like)

        ret: dict[int, dict] = {}

        # Convert entries to :class:`dict`
        for entry in data:
            if key not in entry:
                raise AssetKeyMissingError(key)

            ret[entry[key]] = entry

        return ret

    @staticmethod
    def parse_file(file_like: TextIO) -> dict[int, T]:
        """Parse a file as a :class:`dict` which key is the ID of the value."""
        raise NotImplementedError()
