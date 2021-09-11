"""Classes for handling the castle story asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase, StoryEntryBase

__all__ = ("CastleStoryEntry", "CastleStoryAsset")


@dataclass
class CastleStoryEntry(StoryEntryBase, MasterEntryBase):
    """Single entry of a castle story data."""

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "CastleStoryEntry":
        return CastleStoryEntry(
            id=data["_Id"],
            title_label=data["_Title"]
        )


class CastleStoryAsset(MasterAssetBase[CastleStoryEntry]):
    """Castle story asset class."""

    asset_file_name = "CastleStory.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(CastleStoryParser, file_location, asset_dir=asset_dir, file_like=file_like)


class CastleStoryParser(MasterParserBase[CastleStoryEntry]):
    """Class to parse the castle story file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, CastleStoryEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: CastleStoryEntry.parse_raw(value) for key, value in entries.items()}
