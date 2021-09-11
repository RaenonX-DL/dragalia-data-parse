"""Classes for handling the quest story asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.mono.asset.base import GroupedStoryAssetBase, GroupedStoryEntryBase, MasterEntryBase, MasterParserBase

__all__ = ("QuestStoryEntry", "QuestStoryAsset")


@dataclass
class QuestStoryEntry(GroupedStoryEntryBase, MasterEntryBase):
    """Single entry of a quest story data."""

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "QuestStoryEntry":
        return QuestStoryEntry(
            id=data["_Id"],
            title_label=data["_Title"],
            group_id=data["_GroupId"]
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
    def parse_file(cls, file_like: TextIO) -> dict[int, QuestStoryEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: QuestStoryEntry.parse_raw(value) for key, value in entries.items()}
