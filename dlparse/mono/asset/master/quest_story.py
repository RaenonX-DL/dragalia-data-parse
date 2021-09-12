"""Classes for handling the quest story asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, cast

from dlparse.mono.asset.base import (
    EntryDataType, GroupedStoryAssetBase, GroupedStoryEntryBase, MasterEntryBase, MasterParserBase, ParsedDictIdType,
)

__all__ = ("QuestStoryEntry", "QuestStoryAsset")


@dataclass
class QuestStoryEntry(GroupedStoryEntryBase, MasterEntryBase):
    """Single entry of a quest story data."""

    @staticmethod
    def parse_raw(data: EntryDataType) -> "QuestStoryEntry":
        return QuestStoryEntry(
            id=cast(int, data["_Id"]),
            title_label=cast(str, data["_Title"]),
            group_id=cast(int, data["_GroupId"])
        )


class QuestStoryAsset(GroupedStoryAssetBase[QuestStoryEntry]):
    """Quest story asset class."""

    asset_file_name = "QuestStory.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(QuestStoryParser, file_location, asset_dir=asset_dir, file_like=file_like)


class QuestStoryParser(MasterParserBase[QuestStoryEntry]):
    """Class to parse the quest story file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[ParsedDictIdType, QuestStoryEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: QuestStoryEntry.parse_raw(value) for key, value in entries.items()}
