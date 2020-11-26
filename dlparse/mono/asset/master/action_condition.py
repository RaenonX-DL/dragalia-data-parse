"""Classes for handling the action condition asset."""
from dataclasses import dataclass
from typing import Union, Optional

from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("ActionConditionEntry", "ActionConditionAsset", "ActionConditionParser")


@dataclass
class ActionConditionEntry(MasterEntryBase):
    """Single entry of an action condition data."""

    duration_sec: float
    duration_count: float

    buff_atk: float
    buff_def: float
    buff_crt_rate: float
    buff_crt_damage: float
    buff_skill_damage: float
    buff_sp_rate: float

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "ActionConditionEntry":
        return ActionConditionEntry(
            id=data["_Id"],
            duration_sec=data["_DurationSec"],
            duration_count=data["_DurationNum"],
            buff_atk=data["_RateAttack"],
            buff_def=data["_RateDefense"],
            buff_crt_rate=data["_RateCritical"],
            buff_crt_damage=data["_EnhancedCritical"],
            buff_skill_damage=data["_RateSkill"],
            buff_sp_rate=data["_RateRecoverySp"]
        )


class ActionConditionAsset(MasterAssetBase[ActionConditionEntry]):
    """Action condition asset class."""

    asset_file_name = "ActionCondition.json"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(ActionConditionParser, file_path, asset_dir=asset_dir)


class ActionConditionParser(MasterParserBase[ActionConditionEntry]):
    """Class to parse the action condition file."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, ActionConditionEntry]:
        entries = cls.get_entries(file_path)

        return {key: ActionConditionEntry.parse_raw(value) for key, value in entries.items()}
