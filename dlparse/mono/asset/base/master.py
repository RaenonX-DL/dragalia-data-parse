"""Base object for the master assets."""
import json
from abc import ABC
from dataclasses import dataclass
from typing import Callable, Generic, Optional, TextIO, Type, TypeVar, Union

from dlparse.errors import AssetKeyMissingError
from .asset import AssetBase
from .entry import EntryBase
from .parser import ParserBase

__all__ = ("MasterEntryBase", "MasterAssetBase", "MasterParserBase")


@dataclass
class MasterEntryBase(EntryBase, ABC):
    """Base class for the entries in the master mono behavior asset."""

    id: Union[int, str]  # pylint: disable=invalid-name


T = TypeVar("T", bound=MasterEntryBase)


class MasterParserBase(Generic[T], ParserBase, ABC):
    """Base parser class for parsing the master asset files."""

    @classmethod
    def get_entries_dict(cls, file_like: TextIO) -> dict[Union[int, str], dict]:
        """Get a dict of data entries to be further parsed."""
        data = json.load(file_like)

        if "dict" not in data:
            raise AssetKeyMissingError("dict")
        data = data["dict"]

        if "entriesValue" not in data:
            raise AssetKeyMissingError("dict.entriesValue")
        if "entriesKey" not in data:
            raise AssetKeyMissingError("dict.entriesKey")

        # ``entriesKey`` should not be used as ID because ``_Id`` offset was found in action condition asset
        entry_values = data["entriesValue"][:data["count"]]

        return {entry["_Id"]: entry for entry in entry_values}

    @classmethod
    def get_entries_list(cls, file_like: TextIO) -> list[dict]:
        """Get a list of data entries to be further parsed as a dict."""
        data = json.load(file_like)

        if "list" not in data:
            raise AssetKeyMissingError("list")
        return data["list"]

    @staticmethod
    def parse_file(file_like: str) -> dict[int, T]:
        """Parse a file as a :class:`dict` which key is the ID of the value."""
        raise NotImplementedError()


class MasterAssetBase(Generic[T], AssetBase, ABC):
    """Base class for a master mono behavior asset."""

    def __init__(self, parser_cls: Type[MasterParserBase[T]], file_location: Optional[str] = None, /,
                 asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None):
        super().__init__(parser_cls, file_location, asset_dir=asset_dir, file_like=file_like)

    def __iter__(self):
        return iter(self._data.values())

    def __contains__(self, item):
        return item in self._data.keys()

    @property
    def all_ids(self) -> set[Union[int, str]]:
        """Get the set of all data IDs."""
        return set(self._data.keys())

    def filter(self, condition: Callable[[T], bool]) -> list[T]:
        """Get a list of data which matches the ``condition``."""
        return [data for data in self if condition(data)]

    def get_data_by_id(self, data_id: Union[int, str], default: Optional[T] = None) -> Optional[T]:
        """Get a data by its ``data_id``. Returns ``default`` if not found."""
        return self._data.get(data_id, default)
