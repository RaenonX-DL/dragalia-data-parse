"""Base object for the master assets."""
import json
from abc import ABC
from dataclasses import dataclass
from typing import Type, Optional, Any, Callable, Union, TypeVar

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


class MasterParserBase(ParserBase, ABC):
    """Base parser class for parsing the master asset files."""

    @staticmethod
    def get_entries(file_path: str) -> dict[int, dict]:
        """Get a dict of data entries which value needs to be further parsed."""
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        if "dict" not in data:
            raise AssetKeyMissingError("dict")
        data = data["dict"]

        if "entriesValue" not in data:
            raise AssetKeyMissingError("dict.entriesValue")
        if "entriesKey" not in data:
            raise AssetKeyMissingError("dict.entriesKey")

        entry_keys = filter(lambda key: key != 0, data["entriesKey"])  # Only the entries with key != 0 is valid
        entry_values = data["entriesValue"]

        return dict(zip(entry_keys, entry_values))

    @staticmethod
    def parse_file(file_path: str) -> dict[int, Any]:
        """Parse a file as a :class:`dict` which key is the ID of the value."""
        raise NotImplementedError()


class MasterAssetBase(AssetBase, ABC):
    """Base class for a master mono behavior asset."""

    def __init__(self, parser_cls: Type[MasterParserBase], file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(parser_cls, file_path, asset_dir=asset_dir)

    def __iter__(self):
        return iter(self._data.values())

    def filter(self, condition: Callable[[MasterEntryBase], bool]) -> list[MasterEntryBase]:
        """Get a list of data which matches the ``condition``."""
        return [data for data in self if condition(data)]

    def get_data_by_id(self, data_id: Union[int, str], default: Optional[MasterEntryBase] = None) -> Optional[T]:
        """Get a data by its ``data_id``. Returns ``default`` if not found."""
        return self._data.get(data_id, default)
