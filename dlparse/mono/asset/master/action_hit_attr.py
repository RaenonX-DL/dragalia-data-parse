"""Classes for handling the player action hit attribute asset."""
from dataclasses import dataclass
from typing import Union, Optional

from dlparse.enums import Affliction, HitExecType
from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("HitAttrEntry", "HitAttrAsset", "HitAttrParser")


@dataclass
class HitAttrEntry(MasterEntryBase):
    """Single entry of a hit attribute data."""

    hit_exec_type: HitExecType

    damage_modifier: float

    punisher_states: set[Affliction]  # Rate will be applied when the target has any of the punisher states
    punisher_rate: float

    crisis_limit_rate: float  # 0 = not applicable

    rate_boost_by_buff: float  # 0 = not applicable
    """Damage modifier boosting rate for each buff."""

    break_dmg_rate: float  # Searching regex: "_ToBreakDmgRate": (?!1\.0|0\.0)

    @staticmethod
    def parse_raw(data: dict[str, Union[str, float, int]]) -> "HitAttrEntry":
        punisher_states = {data["_KillerState1"], data["_KillerState2"], data["_KillerState3"]} - {0}
        punisher_states = {Affliction(state) for state in punisher_states} - {Affliction.UNKNOWN}

        return HitAttrEntry(
            id=data["_Id"],
            hit_exec_type=HitExecType(data["_HitExecType"]),
            damage_modifier=data["_DamageAdjustment"],
            punisher_states=punisher_states,
            punisher_rate=data["_KillerStateDamageRate"],
            crisis_limit_rate=data["_CrisisLimitRate"],
            rate_boost_by_buff=data["_DamageUpRateByBuffCount"],
            break_dmg_rate=data["_ToBreakDmgRate"]
        )

    @property
    def has_punisher(self) -> bool:
        """Check if the skill has punisher boosts."""
        return len(self.punisher_states) > 0

    @property
    def boost_by_buff_count(self) -> bool:
        """Check if the damage modifier will be boosted by the count of buffs."""
        return self.rate_boost_by_buff != 0

    @property
    def boost_in_break(self) -> bool:
        """Check if the damage modifier will be boosted during break."""
        return self.break_dmg_rate != 1

    @property
    def change_by_hp(self) -> bool:
        """Check if the mods will be changed based on the character's HP."""
        return self.crisis_limit_rate != 0

    @property
    def deal_damage(self) -> bool:
        """
        Check if the hit actually deals damage.

        Some hits seem to be dummy hit. For example, Renee S1 def down (`DAG_002_03_H03_DEFDOWN_LV03`).
        """
        return self.damage_modifier != 0


class HitAttrAsset(MasterAssetBase):
    """Player action hit attribute asset class."""

    asset_file_name = "PlayerActionhitAttribute.json"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(HitAttrParser, file_path, asset_dir=asset_dir)


class HitAttrParser(MasterParserBase):
    """Class to parse the player action hit attribute file."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, HitAttrEntry]:
        entries = cls.get_entries(file_path)

        return {key: HitAttrEntry.parse_raw(value) for key, value in entries.items()}
