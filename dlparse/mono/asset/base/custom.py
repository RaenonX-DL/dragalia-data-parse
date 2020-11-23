"""Classes for custom assets."""
import json
from abc import ABC
from typing import Any

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
    def get_entries(cls, file_path: str) -> dict[int, dict]:
        """Get a dict of data entries which value needs to be further parsed."""
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        ret: dict[int, dict] = {}

        # Convert entries to :class:`dict`
        for entry in data:
            if cls.key_id not in entry:
                raise AssetKeyMissingError(cls.key_id)

            ret[entry[cls.key_id]] = entry

        return ret

    @staticmethod
    def parse_file(file_path: str) -> dict[int, Any]:
        """Parse a file as a :class:`dict` which key is the ID of the value."""
        raise NotImplementedError()
