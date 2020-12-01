"""Classes for handling the action condition asset."""
from dataclasses import dataclass
from typing import Union, Optional

from dlparse.enums import ElementFlag
from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("ActionConditionEntry", "ActionConditionAsset", "ActionConditionParser")


@dataclass
class ActionConditionEntry(MasterEntryBase):
    """Single entry of an action condition data."""

    duration_sec: float
    duration_count: float
    duration_count_max: int
    """
    Maximum count of the buffs stackable.

    ``0`` means not applicable (``duration_count`` = 0, most likely is a buff limited by time duration).

    ``1`` means unstackable.

    Any positive number means the maximum count of stacks possible.
    """

    probability: float

    buff_atk: float
    buff_def: float
    buff_crt_rate: float
    buff_crt_damage: float
    buff_skill_damage: float
    buff_fs_damage: float
    buff_atk_spd: float
    buff_fs_spd: float
    buff_sp_rate: float

    shield_dmg: float
    shield_hp: float

    elemental_target: ElementFlag

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "ActionConditionEntry":
        duration_count_max = (
            data["_MaxDurationNum"] if data["_IsAddDurationNum"] else 1
            if data["_DurationNum"]
            else 0
        )

        return ActionConditionEntry(
            id=data["_Id"],
            duration_sec=data["_DurationSec"],
            duration_count=data["_DurationNum"],
            duration_count_max=duration_count_max,
            probability=data["_Rate"],
            buff_atk=data["_RateAttack"],
            buff_def=data["_RateDefense"],
            buff_crt_rate=data["_RateCritical"],
            buff_crt_damage=data["_EnhancedCritical"],
            buff_skill_damage=data["_RateSkill"],
            buff_fs_damage=data["_RateBurst"],
            buff_atk_spd=data["_RateAttackSpeed"],
            buff_sp_rate=data["_RateRecoverySp"],
            buff_fs_spd=data["_RateChargeSpeed"],
            shield_dmg=data["_RateDamageShield"],
            shield_hp=data["_RateSacrificeShield"],
            elemental_target=ElementFlag(data["_TargetElemental"])
        )

    @property
    def target_limited_by_element(self):
        """Check if the action condition will be limited by the element of the target."""
        return self.elemental_target.is_effective


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
