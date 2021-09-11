"""Classes for handling the quest story group asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("QuestStoryGroupEntry", "QuestStoryGroupAsset")


@dataclass
class QuestStoryGroupEntry(MasterEntryBase):
    """Single entry of a quest story group data."""

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "QuestStoryGroupEntry":
        return QuestStoryGroupEntry(
            id=data["_Id"],
        )


class QuestStoryGroupAsset(MasterAssetBase[QuestStoryGroupEntry]):
    """Quest story group asset class."""

    asset_file_name = "QuestStoryGroup.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(QuestStoryGroupParser, file_location, asset_dir=asset_dir, file_like=file_like)


class QuestStoryGroupParser(MasterParserBase[QuestStoryGroupEntry]):
    """Class to parse the quest story group file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, QuestStoryGroupEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: QuestStoryGroupEntry.parse_raw(value) for key, value in entries.items()}
