"""Classes for custom assets."""
import json
from abc import ABC
from typing import Any, TextIO

from dlparse.errors import AssetKeyMissingError
from .parser import ParserBase

__all__ = ("CustomParserBase",)


class CustomParserBase(ParserBase, ABC):
    """
    Base parser class for parsing the custom asset files.

    A custom json asset file should be a list of entries.
    Each entries should have a field ``_Id`` to uniquely identifies the corresponding entry.
    """

    key_id: str = "_Id"

    @classmethod
    def get_entries_dict(cls, file_like: TextIO) -> dict[int, dict]:
        """Get a dict of data entries to be further parsed."""
        data = json.load(file_like)

        ret: dict[int, dict] = {}

        # Convert entries to :class:`dict`
        for entry in data:
            if cls.key_id not in entry:
                raise AssetKeyMissingError(cls.key_id)

            ret[entry[cls.key_id]] = entry

        return ret

    @staticmethod
    def parse_file(file_like: TextIO) -> dict[int, Any]:
        """Parse a file as a :class:`dict` which key is the ID of the value."""
        raise NotImplementedError()
