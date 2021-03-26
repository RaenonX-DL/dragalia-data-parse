"""
Classes for handling the enemy data asset.

Note that enemy data and enemy param are different things.
"""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import Element
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("EnemyDataEntry", "EnemyDataAsset")


@dataclass
class EnemyDataEntry(MasterEntryBase):
    """Single entry of an enemy data."""

    element: Element

    od_atk_rate: float
    od_def_rate: float

    bk_duration_sec: int
    bk_def_rate: float

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "EnemyDataEntry":
        return EnemyDataEntry(
            id=data["_Id"],
            element=Element(data["_ElementalType"]),
            od_atk_rate=data["_ObAtkRate"],
            od_def_rate=data["_ObDefRate"],
            bk_duration_sec=data["_BreakDuration"],
            bk_def_rate=data["_BreakDefRate"],
        )


class EnemyDataAsset(MasterAssetBase[EnemyDataEntry]):
    """Enemy data asset class."""

    asset_file_name = "EnemyParam.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(EnemyDataParser, file_location, asset_dir=asset_dir, file_like=file_like)


class EnemyDataParser(MasterParserBase[EnemyDataEntry]):
    """Class to parse the enemy data file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, EnemyDataEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: EnemyDataEntry.parse_raw(value) for key, value in entries.items()}
