"""Classes for handling the player action hit attribute asset."""
from dataclasses import dataclass
from typing import Union, Optional

from dlparse.enums import Affliction, HitExecType, HitTarget
from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("HitAttrEntry", "HitAttrAsset", "HitAttrParser")


@dataclass
class HitAttrEntry(MasterEntryBase):
    """
    Single entry of a hit attribute data.

    This may not actually deal damage.

    For example, functional hit attribute will have an ``damage_modifier`` of 0,
    and link to the buff content using action condition instead.
    """

    hit_exec_type: HitExecType
    target_group: HitTarget

    damage_modifier: float

    is_damage_self: bool
    fix_hp_rate: float

    punisher_states: set[Affliction]  # Rate will be applied when the target has any of the punisher states
    punisher_rate: float

    rate_boost_on_crisis: float  # 0 = not applicable
    """Damage modifier boosting rate on low HP."""
    rate_boost_by_buff: float  # 0 = not applicable
    """Damage modifier boosting rate for each buff."""

    break_dmg_rate: float  # Searching regex: "_ToBreakDmgRate": (?!1\.0|0\.0)

    action_condition_id: int

    sp_recov_ratio: float
    sp_recov_skill_idx_1: int
    sp_recov_skill_idx_2: int

    has_hit_condition: bool
    """
    Check if the hit condition is in effect.

    If this is ``True``, then the skill hit count must be
    greater than or equal to ``hit_condition_lower_bound`` (if set) or
    less than or equal to ``hit_condition_upper_bound`` (if set) to make the hit effective.
    """
    hit_condition_lower_bound: int
    """Lower bound of the hit condition."""
    hit_condition_upper_bound: int
    """Upper bound of the hit condition."""

    @staticmethod
    def parse_raw(data: dict[str, Union[str, float, int]]) -> "HitAttrEntry":
        punisher_states = {data["_KillerState1"], data["_KillerState2"], data["_KillerState3"]} - {0}
        punisher_states = {Affliction(state) for state in punisher_states} - {Affliction.UNKNOWN}

        return HitAttrEntry(
            id=data["_Id"],
            hit_exec_type=HitExecType(data["_HitExecType"]),
            target_group=HitTarget(data["_TargetGroup"]),
            damage_modifier=data["_DamageAdjustment"],
            is_damage_self=bool(data["_IsDamageMyself"]),
            fix_hp_rate=data["_SetCurrentHpRate"],
            punisher_states=punisher_states,
            punisher_rate=data["_KillerStateDamageRate"],
            rate_boost_on_crisis=data["_CrisisLimitRate"],
            rate_boost_by_buff=data["_DamageUpRateByBuffCount"],
            break_dmg_rate=data["_ToBreakDmgRate"],
            action_condition_id=data["_ActionCondition1"],
            sp_recov_ratio=data["_RecoverySpRatio"],
            sp_recov_skill_idx_1=data["_RecoverySpSkillIndex"],
            sp_recov_skill_idx_2=data["_RecoverySpSkillIndex2"],
            has_hit_condition=data["_HitConditionType"] != 0,
            hit_condition_lower_bound=data["_HitConditionP1"],
            hit_condition_upper_bound=data["_HitConditionP2"]
        )

    @property
    def has_action_condition(self):
        """
        Check if this hit attribute has action condition labeled.

        .. note::
            Action condition contains the information of afflicting the target or buffs.
        """
        return self.action_condition_id != 0

    @property
    def boost_on_target_afflicted(self) -> bool:
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
    def boost_by_hp(self) -> bool:
        """Check if the mods will be changed based on the character's HP."""
        return self.rate_boost_on_crisis != 0

    @property
    def deals_damage(self) -> bool:
        """
        Check if the hit actually deals damage.

        Some hits seem to be dummy hit. For example, Renee S1 def down (`DAG_002_03_H03_DEFDOWN_LV03`).
        """
        return self.damage_modifier != 0


class HitAttrAsset(MasterAssetBase[HitAttrEntry]):
    """Player action hit attribute asset class."""

    asset_file_name = "PlayerActionhitAttribute.json"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(HitAttrParser, file_path, asset_dir=asset_dir)


class HitAttrParser(MasterParserBase[HitAttrEntry]):
    """Class to parse the player action hit attribute file."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, HitAttrEntry]:
        entries = cls.get_entries(file_path)

        return {key: HitAttrEntry.parse_raw(value) for key, value in entries.items()}
