"""Classes for handling the text label asset."""
from dataclasses import dataclass
from typing import TextIO, cast

from dlparse.mono.asset.base import (
    CustomParserBase, EntryDataType, MasterAssetIdType, MasterEntryBase, MasterParserBase,
    MultilingualAssetBase, TextEntryBase,
)

__all__ = ("TextEntry", "TextAssetMultilingual")


@dataclass
class TextEntry(TextEntryBase, MasterEntryBase):
    """Single entry of a text label."""

    @staticmethod
    def parse_raw(data: EntryDataType) -> "TextEntry":
        return TextEntry(
            id=cast(str, data["_Id"]),
            text=cast(str, data["_Text"]),
        )


class MasterTextParser(MasterParserBase[TextEntry]):
    """Class to parse the master text label file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[MasterAssetIdType, TextEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: TextEntry.parse_raw(value) for key, value in entries.items()}


class CustomTextParser(CustomParserBase[TextEntry]):
    """Class to parse the custom text label file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[MasterAssetIdType, TextEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: TextEntry.parse_raw(value) for key, value in entries.items()}


class TextAssetMultilingual(MultilingualAssetBase[TextEntry]):
    """Multilingual text asset class."""

    # pylint: disable=too-few-public-methods

    def __init__(self, asset_dir: str):
        super().__init__(MasterTextParser, asset_dir, "TextLabel")
