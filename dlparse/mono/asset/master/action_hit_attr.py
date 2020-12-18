"""Classes for handling the player action hit attribute asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import HitExecType, HitTarget, Status
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

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
    damage_modifier_counter: float
    """
    Damage modifier to be added if the user is damaged during skill casting.

    Note that this damage is calculated element-neutrally.
    The formula of this is simply ``damage received x counter damage modifier``.
    Any additional effects such as crisis mods, punishers will **NOT** be applied.
    """

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
    buff_boost_data_id: int  # 0 = not applicable
    """ID of the buff boost data. This ID will be used to get the buff boost data from the buff count data asset."""

    action_condition_id: int

    sp_recov_ratio: float
    sp_recov_skill_idx_1: int
    sp_recov_skill_idx_2: int

    dummy_hit_count: bool
    """
    Check if a dummy hit count will be added according to the count of teammates covered by the skill effect.

    Check ``notes/others/TeammateCoverageHandling.md`` for more details.
    """

    has_hit_condition: bool
    """
    Check if the hit condition is in effect.

    Check ``notes/others/TeammateCoverageHandling.md`` for more details
    as this field is related to the handling of such.

    - Hit condition means that the hit count of the skill must match a certain criteria
    (composed by `hit_condition_lower_bound` and `hit_condition_upper_bound`) to make the hit attribute effective.
    """
    hit_condition_lower_bound: int
    """Lower bound of the hit condition."""
    hit_condition_upper_bound: int
    """Upper bound of the hit condition."""

    @staticmethod
    def parse_raw(data: dict[str, Union[str, float, int]]) -> "HitAttrEntry":
        punisher_states = {data["_KillerState1"], data["_KillerState2"], data["_KillerState3"]} - {0}
        punisher_states = {Status(state) for state in punisher_states} - {Status.UNKNOWN}

        # As of 2020/12/12, if `data["_HitConditionType"]` is a non-zero value, it can only be either `1` or `2`.
        # For hit condition = 1, it's only used by Laranoa S2 (`106502012`) to indicate the teammate count.
        # For hit condition = 2, it's only used by Summer Cleo S2 (`106504012`), Nadine S1 (`105501021`),
        # and Chelle S1 (`106505031`).

        return HitAttrEntry(
            id=data["_Id"],
            hit_exec_type=HitExecType(data["_HitExecType"]),
            target_group=HitTarget(data["_TargetGroup"]),
            damage_modifier=data["_DamageAdjustment"],
            damage_modifier_counter=data["_DamageCounterCoef"],
            rate_boost_in_od=data["_ToOdDmgRate"],
            rate_boost_in_bk=data["_ToBreakDmgRate"],
            is_damage_self=bool(data["_IsDamageMyself"]),
            hp_fix_rate=data["_SetCurrentHpRate"],
            hp_consumption_rate=data["_ConsumeHpRate"],
            punisher_states=punisher_states,
            punisher_rate=data["_KillerStateDamageRate"],
            rate_boost_on_crisis=data["_CrisisLimitRate"],
            rate_boost_by_buff=data["_DamageUpRateByBuffCount"],
            buff_boost_data_id=data["_DamageUpDataByBuffCount"],
            action_condition_id=data["_ActionCondition1"],
            sp_recov_ratio=data["_RecoverySpRatio"],
            sp_recov_skill_idx_1=data["_RecoverySpSkillIndex"],
            sp_recov_skill_idx_2=data["_RecoverySpSkillIndex2"],
            dummy_hit_count=bool(data["_IsAddCombo"]),
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
    def is_hit_condition_range(self) -> bool:
        """
        Check if the hit condition is a range.

        If this holds, the hit count must fall within the hit coundition boundaries
        to make the hit attribute effective.

        Note that if this holds, ``self.is_hit_condition_gte`` always holds.
        Because of this, whenever hit condition is be used,
        always check for this before ``self.is_hit_condition_gte`` to avoid errors.
        """
        return bool(self.hit_condition_upper_bound and self.hit_condition_lower_bound)

    @property
    def is_hit_condition_gte(self) -> bool:
        """
        Check if the hit condition is a threshold.

        If this holds, the hit count must fall within the hit coundition boundaries
        to make the hit attribute effective.

        Note that if ``self.is_hit_condition_range`` holds, this always holds.
        Because of this, whenever hit condition is be used,
        always check for ``self.is_hit_condition_range`` before this to avoid errors.
        """
        return self.hit_condition_lower_bound and not self.hit_condition_upper_bound

    def is_effective_hit_count(self, hit_count: int) -> bool:
        """Check if the hit attribute is effective when the user's hit count is ``hit_count``."""
        if not self.has_hit_condition:
            # Always effective if no hit condition
            return True

        is_within_range = (self.is_hit_condition_range
                           and self.hit_condition_lower_bound <= hit_count <= self.hit_condition_upper_bound)
        is_greater_than_threshold = self.is_hit_condition_gte and hit_count >= self.hit_condition_lower_bound

        return is_within_range or is_greater_than_threshold

    @property
    def boost_on_target_afflicted(self) -> bool:
        """Check if the skill has punisher boosts."""
        return len(self.punisher_states) > 0

    @property
    def boost_by_buff_count(self) -> bool:
        """Check if the damage modifier will be boosted by the count of buffs."""
        return self.rate_boost_by_buff != 0 or self.buff_boost_data_id != 0

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

    def is_effective_to_enemy(self, desired_effectiveness: bool) -> bool:
        """
        Check if the hit is effective to the enemy.

        If any of the conditions below holds, the hit is considered effective:

        - Afflict the enemy

        - Deals damage to the enemy
        """
        # Known priority rules:
        # - Dummy hit count > Hit exec type
        #   - For Nadine S1 (`105501021`), the label used for counting the dummy hit is considered as buffing hit.
        #     However, such hit should not be considered as *not effective* to the enemy such early.
        # - Hit exec type > Damage modifier
        #   - For Dragonyule Nefaria S2 (`106402022`), buffing hit attributes have damage modifiers,
        #     although seems not used. Such hit must be considered as *ineffective* to the enemy.

        if self.dummy_hit_count:
            # If the hit attribute adds dummy hit count, return the desired effectiveness because
            # the hit data should be considered regardless its effect target
            # -----------------------------------------------------------------------------------
            # Simply returning `True` or `False`, gives inaccurate result for either attacking or supportive skill data
            # because the hit to add dummy counts will be missed.
            # Therefore, returning the desired effectiveness to keep the effectiveness being the desired one
            return desired_effectiveness

        if self.hit_exec_type not in (HitExecType.DAMAGE, HitExecType.UNKNOWN):
            # Not dealing damage
            # > Some hit attributes (`BOW_CHR_09_H01_TENSION_LV03` and `BOW_CHR_09_H02_SIELD_LV03` of Nefaria S2
            # > (`106402022`) has damage modifier yet it's a buffing hit
            return False

        if self.damage_modifier:
            # Deals damage
            return True

        if self.target_group != HitTarget.ENEMY:
            # Has action condition but the target is not enemy
            return False

        if not self.has_action_condition:
            # No action condition assigned & does not have action condition binded
            return False

        return True


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
