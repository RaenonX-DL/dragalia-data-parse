"""Classes for handling the quest data asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import Element, QuestMode
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("QuestDataEntry", "QuestDataAsset")


@dataclass
class QuestDataEntry(MasterEntryBase):
    """Single entry of a quest data."""

    name_view_label: str

    quest_mode: QuestMode

    element_1: Element
    element_1_limit: Element
    element_2: Element
    element_2_limit: Element

    max_time_sec: int
    max_revive: int

    variation_idx: int  # 1-based index
    area_1_name: str

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "QuestDataEntry":
        return QuestDataEntry(
            id=data["_Id"],
            quest_mode=QuestMode(data["_QuestPlayModeType"]),
            name_view_label=data["_QuestViewName"],
            element_1=Element(data["_Elemental"]),
            element_1_limit=Element(data["_LimitedElementalType"]),
            element_2=Element(data["_Elemental2"]),
            element_2_limit=Element(data["_LimitedElementalType2"]),
            max_time_sec=data["_FailedTermsTimeElapsed"],
            max_revive=data["_RebornLimit"],
            variation_idx=data["_VariationType"],
            area_1_name=data["_AreaName01"]
        )


class QuestDataAsset(MasterAssetBase[QuestDataEntry]):
    """Quest data asset class."""

    asset_file_name = "QuestData.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(QuestDataParser, file_location, asset_dir=asset_dir, file_like=file_like)


class QuestDataParser(MasterParserBase[QuestDataEntry]):
    """Class to parse the quest data file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, QuestDataEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: QuestDataEntry.parse_raw(value) for key, value in entries.items()}
