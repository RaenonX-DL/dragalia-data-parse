"""Classes for handling the player action hit attribute asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import HitExecType, HitTarget, Status
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase
from .action_condition import ActionConditionAsset

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
    hp_fix_rate: float
    hp_consumption_rate: float

    # Rate will be applied when the target has any of the punisher states
    # The rate will only apply once, even if the target have multiple states that are listed as punisher
    punisher_states: set[Status]
    punisher_rate: float

    rate_boost_in_od: float  # 1 = No change
    """Damage modifier boosting rate if the target is in Overdrive (OD) state."""
    rate_boost_in_bk: float  # 1 = No change
    """Damage modifier boosting rate if the target is in Break (BK) state."""
    rate_boost_on_crisis: float  # 0 = not applicable
    """
    Damage modifier boosting rate on 1 HP.

    This is quadratic. For the detailed calculation, check the documentation of ``calculate_crisis_mod()``.
    """
    rate_boost_by_buff: float  # 0 = not applicable
    """Damage modifier boosting rate for each buff."""

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
    def boost_in_od(self) -> bool:
        """Check if the damage modifier will be boosted during overdrive (OD)."""
        return self.damage_modifier and self.rate_boost_in_od != 1

    @property
    def boost_in_bk(self) -> bool:
        """Check if the damage modifier will be boosted during break (BK)."""
        return self.damage_modifier and self.rate_boost_in_bk != 1

    @property
    def boost_by_hp(self) -> bool:
        """Check if the mods will be changed based on the character's HP."""
        return self.rate_boost_on_crisis != 0

    def is_effective_to_enemy(self, asset_action_cond: ActionConditionAsset) -> bool:
        """
        Check if the hit is effective to the enemy.

        If any of the conditions below holds, the hit is considered effective:

        - Afflict the enemy

        - Deals damage to the enemy
        """
        if self.damage_modifier:
            # Deals damage
            return True

        if not self.has_action_condition:
            # No action condition assigned & does not have action condition binded
            return False

        if self.target_group != HitTarget.ENEMY:
            # Has action condition but the target is not enemy
            return False

        action_cond_data = asset_action_cond.get_data_by_id(self.action_condition_id)

        return action_cond_data.afflict_status.is_abnormal_status

    @staticmethod
    def parse_raw(data: dict[str, Union[str, float, int]]) -> "HitAttrEntry":
        punisher_states = {data["_KillerState1"], data["_KillerState2"], data["_KillerState3"]} - {0}
        punisher_states = {Status(state) for state in punisher_states} - {Status.UNKNOWN}

        return HitAttrEntry(
            id=data["_Id"],
            hit_exec_type=HitExecType(data["_HitExecType"]),
            target_group=HitTarget(data["_TargetGroup"]),
            damage_modifier=data["_DamageAdjustment"],
            rate_boost_in_od=data["_ToOdDmgRate"],
            rate_boost_in_bk=data["_ToBreakDmgRate"],
            is_damage_self=bool(data["_IsDamageMyself"]),
            hp_fix_rate=data["_SetCurrentHpRate"],
            hp_consumption_rate=data["_ConsumeHpRate"],
            punisher_states=punisher_states,
            punisher_rate=data["_KillerStateDamageRate"],
            rate_boost_on_crisis=data["_CrisisLimitRate"],
            rate_boost_by_buff=data["_DamageUpRateByBuffCount"],
            action_condition_id=data["_ActionCondition1"],
            sp_recov_ratio=data["_RecoverySpRatio"],
            sp_recov_skill_idx_1=data["_RecoverySpSkillIndex"],
            sp_recov_skill_idx_2=data["_RecoverySpSkillIndex2"],
            has_hit_condition=data["_HitConditionType"] != 0,
            hit_condition_lower_bound=data["_HitConditionP1"],
            hit_condition_upper_bound=data["_HitConditionP2"]
        )


class HitAttrAsset(MasterAssetBase[HitAttrEntry]):
    """Player action hit attribute asset class."""

    asset_file_name = "PlayerActionHitAttribute.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(HitAttrParser, file_location, asset_dir=asset_dir, file_like=file_like)


class HitAttrParser(MasterParserBase[HitAttrEntry]):
    """Class to parse the player action hit attribute file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, HitAttrEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: HitAttrEntry.parse_raw(value) for key, value in entries.items()}
