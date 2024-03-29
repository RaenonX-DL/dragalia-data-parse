"""Condition composite class."""
from dataclasses import dataclass, field
from typing import Iterable, Optional, TYPE_CHECKING, Union

from dlparse.enums.condition_base import ConditionCompositeBase
from dlparse.errors import ConditionValidationFailedError
from dlparse.utils import remove_duplicates_preserve_order
from .category import ConditionCategories as CondCat, ConditionCheckResult
from .items import Condition
from .validate import validate_conditions
# Relative import to avoid circular import
from ..action_debuff_type import ActionDebuffType
from ..element import Element
from ..status import Status
from ..weapon import Weapon

if TYPE_CHECKING:
    from dlparse.mono.asset import BuffCountAsset, HitAttrEntry

__all__ = ("ConditionComposite",)

COMP_UNCATEGORIZED_EXCEPTION: set[Condition] = {
    # None condition
    Condition.NONE,
    # Special self status
    Condition.SELF_SHAPESHIFT_COMPLETED,
    Condition.SELF_PASSIVE_ENHANCED,
    # Upon skill usage
    Condition.SKILL_USED_S1,
    Condition.SKILL_USED_S2,
    Condition.SKILL_USED_ALL,
    # Misc
    Condition.MARK_EXPLODES,
    Condition.COUNTER_RED_ATTACK,
    Condition.QUEST_START
}


# ``eq=False`` to keep the ``__hash__`` of the superclass
# ``repr=False`` to keep the ``__repr__`` of the superclass
@dataclass(eq=False, repr=False)
class ConditionComposite(ConditionCompositeBase[Condition]):
    """Composite class of various attacking conditions."""

    # region Target
    target_afflictions: set[Condition] = field(init=False)
    target_afflictions_converted: set[Status] = field(init=False)
    target_element: Optional[Condition] = field(init=False)
    target_element_converted: Element = field(init=False)
    target_infliction: Optional[Condition] = field(init=False)
    target_infliction_converted: Status = field(init=False)
    target_in_od: bool = field(init=False)
    target_in_bk: bool = field(init=False)
    target_debuff: Optional[Condition] = field(init=False)
    target_debuff_converted: ActionDebuffType = field(init=False)
    # endregion

    # region Self status
    hp_status: Optional[Condition] = field(init=False)
    hp_status_converted: float = field(init=False)
    hp_condition: Optional[Condition] = field(init=False)
    combo_count: Optional[Condition] = field(init=False)
    combo_count_converted: int = field(init=False)
    buff_count: Optional[Condition] = field(init=False)
    buff_count_converted: int = field(init=False)
    buff_field_self: Optional[Condition] = field(init=False)
    buff_field_self_converted: int = field(init=False)
    buff_field_ally: Optional[Condition] = field(init=False)
    buff_field_ally_converted: int = field(init=False)
    weapon_type: Optional[Condition] = field(init=False)
    weapon_type_converted: Weapon = field(init=False)
    action_cond: Optional[Condition] = field(init=False)
    action_cond_id: int = field(init=False)
    action_cond_lv: Optional[Condition] = field(init=False)
    action_cond_lv_converted: int = field(init=False)
    gauge_filled: Optional[Condition] = field(init=False)
    gauge_filled_converted: int = field(init=False)
    shapeshift_count: Optional[Condition] = field(init=False)
    shapeshift_count_converted: int = field(init=False)
    in_dragon_count: Optional[Condition] = field(init=False)
    in_dragon_count_converted: int = field(init=False)
    is_energized: bool = field(init=False)
    is_team_amp_up: bool = field(init=False)
    is_passive_enhanced: bool = field(init=False)
    current_mode: Optional[Condition] = field(init=False)
    current_mode_idx: int = field(init=False)
    # endregion

    # region Skill effect / animation
    teammate_coverage: Optional[Condition] = field(init=False)
    teammate_coverage_converted: int = field(init=False)
    bullet_hit_count: Optional[Condition] = field(init=False)
    bullet_hit_count_converted: int = field(init=False)
    bullets_on_map: Optional[Condition] = field(init=False)
    bullets_on_map_converted: int = field(init=False)
    bullets_summoned: Optional[Condition] = field(init=False)
    bullets_summoned_converted: int = field(init=False)
    addl_inputs: Optional[Condition] = field(init=False)
    addl_inputs_converted: int = field(init=False)
    action_cancel: Optional[Condition] = field(init=False)
    action_counter_red: bool = field(init=False)
    mark_explode: bool = field(init=False)
    # endregion

    # region Other fields
    trigger: Condition = field(init=False)
    probability: Condition = field(init=False)
    probability_converted: float = field(init=False)
    # endregion

    # region Other fields (hidden)
    _has_buff_boost_condition: bool = field(init=False)

    # endregion

    @staticmethod
    def _init_validate_conditions(conditions: tuple[Condition]):
        # Validate the condition combinations
        if result := not validate_conditions(conditions):
            raise ConditionValidationFailedError(result)

    def _init_validate_target(self):
        # Check `self.afflictions_condition`
        if any(condition not in CondCat.target_status
               for condition in self.target_afflictions):
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_AFFLICTION_ONLY)

        # Check `self.target_element`
        if self.target_element and self.target_element not in CondCat.target_element:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_TARGET_ELEMENT)

        # Check `self.target_debuff`
        if self.target_debuff and self.target_debuff not in CondCat.target_debuff:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_TARGET_DEBUFF)

    def _init_validate_self_general(self):
        # Check `self.hp_status`
        if self.hp_status and self.hp_status not in CondCat.self_hp_status:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_HP_STATUS)

        # Check `self.hp_condition`
        if self.hp_condition and self.hp_condition not in CondCat.self_hp_cond:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_HP_CONDITION)

        # Check `self.combo_count`
        if self.combo_count and self.combo_count not in CondCat.self_combo_count:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_COMBO_COUNT)

        # Check `self.buff_count`
        if self.buff_count and self.buff_count not in CondCat.self_buff_count:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_BUFF_COUNT)

        # Check `self.bullet_hit_count`
        if self.bullet_hit_count and self.bullet_hit_count not in CondCat.skill_bullet_hit:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_BULLET_HIT_COUNT)

        # Check `self.buff_field_self`
        if self.buff_field_self and self.buff_field_self not in CondCat.self_in_buff_field_self:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_BUFF_FIELD_SELF)

        # Check `self.buff_field_ally`
        if self.buff_field_ally and self.buff_field_ally not in CondCat.self_in_buff_field_ally:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_BUFF_FIELD_ALLY)

    def _init_validate_self_special(self):
        # Check `self.action_cond`
        if self.action_cond and self.action_cond not in CondCat.action_condition:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_ACTION_CONDITION)

        if self.action_cond_lv and self.action_cond_lv not in CondCat.self_action_cond_lv:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_ACTION_COND_LV)

        # Check `self.gauge_filled`
        if self.gauge_filled and self.gauge_filled not in CondCat.self_gauge_filled:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_GAUGE_FILLED)

        # Check `self.shapeshift_count`
        if self.shapeshift_count and self.shapeshift_count not in CondCat.shapeshifted_count:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_SHAPESHIFT_COUNT)

        # Check `self.in_dragon_count`
        if self.in_dragon_count and self.in_dragon_count not in CondCat.in_dragon_count:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_SHAPESHIFT_COUNT_IN_DRAGON)

    def _init_validate_skill(self):
        # Check `self.teammate_coverage`
        if self.teammate_coverage and self.teammate_coverage not in CondCat.skill_teammates_covered:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_TEAMMATE_COVERAGE)

        # Check `self.bullet_hit_count`
        if self.bullet_hit_count and self.bullet_hit_count not in CondCat.skill_bullet_hit:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_BULLET_HIT_COUNT)

        # Check `self.bullets_on_map`
        if self.bullets_on_map and self.bullets_on_map not in CondCat.skill_bullets_on_map:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_BULLETS_ON_MAP)

        # Check `self.bullets_summoned`
        if self.bullets_summoned and self.bullets_summoned not in CondCat.skill_bullets_summoned:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_BULLETS_SUMMONED)

        # Check `self.addl_inputs`
        if self.addl_inputs and self.addl_inputs not in CondCat.skill_addl_inputs:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_ADDL_INPUTS)

        # Check `self.action_canceling`
        if self.action_cancel and self.action_cancel not in CondCat.skill_action_cancel:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_ACTION_CANCEL)

    def _init_validate_others(self):
        # Check `self.trigger`
        if self.trigger and self.trigger not in CondCat.trigger:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_TRIGGER)

        # Check `self.probability`
        if self.probability and self.probability not in CondCat.probability:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_PROBABILITY)

    def _init_validate_fields(self, conditions: tuple[Condition]):
        self._init_validate_target()
        self._init_validate_self_general()
        self._init_validate_self_special()
        self._init_validate_skill()
        self._init_validate_others()

        if cond_not_categorized := (set(conditions) - set(self.conditions_sorted) - COMP_UNCATEGORIZED_EXCEPTION):
            raise ConditionValidationFailedError(ConditionCheckResult.HAS_CONDITIONS_LEFT, cond_not_categorized)

    def _init_categorized_condition_fields(self, conditions: Optional[Union[Iterable[Condition], Condition]]):
        # region Target status
        self.target_afflictions = CondCat.target_status.extract(conditions)
        self.target_element = CondCat.target_element.extract(conditions)
        self.target_infliction = CondCat.target_status_infliction.extract(conditions)
        self.target_in_od = Condition.TARGET_OD_STATE in conditions
        self.target_in_bk = Condition.TARGET_BK_STATE in conditions
        self.target_debuff = CondCat.target_debuff.extract(conditions)
        # endregion

        # region Self status
        self.hp_status = CondCat.self_hp_status.extract(conditions)
        self.hp_condition = CondCat.self_hp_cond.extract(conditions)
        self.combo_count = CondCat.self_combo_count.extract(conditions)
        self.buff_count = CondCat.self_buff_count.extract(conditions)
        self.buff_field_self = CondCat.self_in_buff_field_self.extract(conditions)
        self.buff_field_ally = CondCat.self_in_buff_field_ally.extract(conditions)
        self.weapon_type = CondCat.self_weapon_type.extract(conditions)
        self.action_cond = CondCat.action_condition.extract(conditions)
        self.action_cond_lv = CondCat.self_action_cond_lv.extract(conditions)
        self.gauge_filled = CondCat.self_gauge_filled.extract(conditions)
        self.shapeshift_count = CondCat.shapeshifted_count.extract(conditions)
        self.in_dragon_count = CondCat.in_dragon_count.extract(conditions)
        self.current_mode = CondCat.current_mode.extract(conditions)
        self.is_energized = Condition.SELF_ENERGIZED in conditions
        self.is_team_amp_up = Condition.SELF_TEAM_AMP_UP in conditions
        self.is_passive_enhanced = Condition.SELF_PASSIVE_ENHANCED in conditions
        # endregion

        # region Skill effect / animation
        self.teammate_coverage = CondCat.skill_teammates_covered.extract(conditions)
        self.bullet_hit_count = CondCat.skill_bullet_hit.extract(conditions)
        self.bullets_on_map = CondCat.skill_bullets_on_map.extract(conditions)
        self.bullets_summoned = CondCat.skill_bullets_summoned.extract(conditions)
        self.addl_inputs = CondCat.skill_addl_inputs.extract(conditions)
        self.action_cancel = CondCat.skill_action_cancel.extract(conditions)
        self.action_counter_red = Condition.COUNTER_RED_ATTACK in conditions
        self.mark_explode = Condition.MARK_EXPLODES in conditions
        # endregion

        # region Others
        self.trigger = CondCat.trigger.extract(conditions)
        self.probability = CondCat.probability.extract(conditions)
        # endregion

    def _init_converted_fields(self):
        # region Target status
        self.target_afflictions_converted = {
            CondCat.target_status.convert(condition) for condition in self.target_afflictions
        }
        self.target_element_converted = CondCat.target_element.convert(self.target_element, on_missing=None)
        self.target_infliction_converted = CondCat.target_status_infliction.convert(
            self.target_infliction, on_missing=None
        )
        self.target_debuff_converted = CondCat.target_debuff.convert(self.target_debuff, on_missing=None)
        # endregion

        # region Self status
        self.hp_status_converted = CondCat.self_hp_status.convert(self.hp_status, on_missing=1)
        self.combo_count_converted = CondCat.self_combo_count.convert(self.combo_count, on_missing=0)
        self.buff_count_converted = CondCat.self_buff_count.convert(self.buff_count, on_missing=0)
        self.buff_field_self_converted = CondCat.self_in_buff_field_self.convert(self.buff_field_self, on_missing=0)
        self.buff_field_ally_converted = CondCat.self_in_buff_field_ally.convert(self.buff_field_ally, on_missing=0)
        self.weapon_type_converted = CondCat.self_weapon_type.convert(self.weapon_type, on_missing=None)
        self.action_cond_id = CondCat.action_condition.convert(self.action_cond, on_missing=None)
        self.action_cond_lv_converted = CondCat.self_action_cond_lv.convert(self.action_cond_lv, on_missing=0)
        self.gauge_filled_converted = CondCat.self_gauge_filled.convert(self.gauge_filled, on_missing=0)
        self.shapeshift_count_converted = CondCat.shapeshifted_count.convert(self.shapeshift_count, on_missing=0)
        self.in_dragon_count_converted = CondCat.in_dragon_count.convert(self.in_dragon_count, on_missing=0)
        self.current_mode_idx = CondCat.current_mode.convert(self.current_mode, on_missing=False)
        # endregion

        # region Skill effect / animation
        self.teammate_coverage_converted = CondCat.skill_teammates_covered.convert(
            self.teammate_coverage, on_missing=None
        )
        self.bullet_hit_count_converted = CondCat.skill_bullet_hit.convert(self.bullet_hit_count, on_missing=None)
        self.bullets_on_map_converted = CondCat.skill_bullets_on_map.convert(self.bullets_on_map, on_missing=None)
        self.bullets_summoned_converted = CondCat.skill_bullets_summoned.convert(
            self.bullets_summoned, on_missing=None
        )
        # 0 instead of 1 to trigger the error faster if attempting to compare when additional input is not available
        self.addl_inputs_converted = CondCat.skill_addl_inputs.convert(self.addl_inputs, on_missing=None)
        # endregion

        # region Others
        self.probability_converted = CondCat.probability.convert(self.probability, on_missing=1)
        # endregion

    def __post_init__(self, conditions: Optional[Union[Iterable[Condition], Condition]]):
        conditions = self._init_process_conditions(conditions)

        self._init_categorized_condition_fields(conditions)
        self._init_validate_fields(conditions)
        self._init_converted_fields()

        # region Private fields
        self._has_buff_boost_condition = any(
            condition in CondCat.self_buff_count or condition in CondCat.self_lapis_card
            for condition in conditions
        )
        # endregion

    def _cond_sorted_target(self) -> tuple[Condition]:
        ret: tuple[Condition] = tuple(sorted(self.target_afflictions))

        if self.target_element:
            ret += (self.target_element,)

        if self.target_infliction:
            ret += (self.target_infliction,)

        if self.target_in_od:
            ret += (Condition.TARGET_OD_STATE,)

        if self.target_in_bk:
            ret += (Condition.TARGET_BK_STATE,)

        if self.target_debuff:
            ret += (self.target_debuff,)

        return ret

    def _cond_sorted_self_general(self) -> tuple[Condition]:
        ret: tuple[Condition] = tuple()

        if self.hp_status:
            ret += (self.hp_status,)

        if self.hp_condition:
            ret += (self.hp_condition,)

        if self.combo_count:
            ret += (self.combo_count,)

        if self.buff_count:
            ret += (self.buff_count,)

        if self.buff_field_self:
            ret += (self.buff_field_self,)

        if self.buff_field_ally:
            ret += (self.buff_field_ally,)

        return ret

    def _cond_sorted_self_special(self) -> tuple[Condition]:
        ret: tuple[Condition] = tuple()

        if self.action_cond:
            ret += (self.action_cond,)

        if self.action_cond_lv:
            ret += (self.action_cond_lv,)

        if self.gauge_filled:
            ret += (self.gauge_filled,)

        if self.shapeshift_count:
            ret += (self.shapeshift_count,)

        if self.current_mode:
            ret += (self.current_mode,)

        if self.in_dragon_count:
            ret += (self.in_dragon_count,)

        if self.is_energized:
            ret += (Condition.SELF_ENERGIZED,)

        if self.is_team_amp_up:
            ret += (Condition.SELF_TEAM_AMP_UP,)

        if self.is_passive_enhanced:
            ret += (Condition.SELF_PASSIVE_ENHANCED,)

        return ret

    def _cond_sorted_skill(self) -> tuple[Condition]:
        ret: tuple[Condition] = tuple()

        if self.bullet_hit_count:
            ret += (self.bullet_hit_count,)

        if self.teammate_coverage:
            ret += (self.teammate_coverage,)

        if self.bullets_on_map:
            ret += (self.bullets_on_map,)

        if self.bullets_summoned:
            ret += (self.bullets_summoned,)

        if self.addl_inputs:
            ret += (self.addl_inputs,)

        if self.action_cancel:
            ret += (self.action_cancel,)

        if self.action_counter_red:
            ret += (Condition.COUNTER_RED_ATTACK,)

        if self.mark_explode:
            ret += (Condition.MARK_EXPLODES,)

        return ret

    def _cond_sorted_others(self) -> tuple[Condition]:
        ret: tuple[Condition] = tuple()

        if self.trigger:
            ret += (self.trigger,)

        if self.probability:
            ret += (self.probability,)

        return ret

    @property
    def has_buff_boost_condition(self) -> bool:
        """Check if the composite has any condition that boosts damage by the buff count."""
        return self._has_buff_boost_condition

    @property
    def conditions_sorted(self) -> tuple[Condition, ...]:
        """
        Get the sorted conditions as a tuple.

        Conditions will be sorted in the following order:

        - [Target] Afflictions
        - [Target] Target element
        - [Self] HP status / condition
        - [Self] Combo count
        - [Self] Buff count
        - [Self] Buff field built by self / ally
        - [Self] Action condition / Action condition level
        - [Self] Gauge status
        - [Self] Shapeshift
        - [Skill] Bullet hit count
        - [Skill] Teammate coverage
        - [Skill] Bullets on map
        - [Skill] Additional inputs
        - [Skill] Action canceling
        - [Skill] Action countering
        - [Skill] Mark explosion
        - [Other] Trigger
        - [Other] Probability
        """
        # ``Condition.TARGET_DEF_DOWN`` is categorized into both target status and debuff.
        # Sorted conditions may yield this condition twice. Therefore removing the duplicates.

        conditions: tuple[Condition, ...] = (self._cond_sorted_target()
                                             + self._cond_sorted_self_general()
                                             + self._cond_sorted_self_special()
                                             + self._cond_sorted_skill()
                                             + self._cond_sorted_others())

        return remove_duplicates_preserve_order(conditions)

    def get_boost_rate_by_buff(self, hit_attr: "HitAttrEntry", asset_buff_count: "BuffCountAsset"):
        """Get the damage boost rate of ``hit_attr`` under the given condition."""
        if hit_attr.buff_boost_data_id:
            # Uses buff boost data to boost the damage
            return asset_buff_count.get_data_by_id(hit_attr.buff_boost_data_id).get_buff_up_rate(self)

        # Get the uncapped buff boost rate
        return self.buff_count_converted * hit_attr.rate_boost_by_buff

    def __iter__(self):
        return iter(self.conditions_sorted)

    def __bool__(self):
        return bool(self.conditions_sorted)

    def __add__(self, other: Union["ConditionComposite", Condition, None]):
        if other is None:
            return self

        if isinstance(other, Condition):
            other = ConditionComposite(other)

        if not isinstance(other, ConditionComposite):
            raise TypeError(f"Cannot add `ConditionComposite` with type {type(other)}")

        return ConditionComposite(self.conditions_sorted + other.conditions_sorted)

    def __contains__(self, item: Union["ConditionComposite", Condition]):
        if isinstance(item, Condition):
            item = ConditionComposite(item)

        if not isinstance(item, ConditionComposite):
            raise TypeError(f"Cannot check if {item} ({type(item)}) contains this `ConditionComposite`")

        return set(item) - set(self) == set()

    def __lt__(self, other):
        if not isinstance(other, ConditionComposite):
            raise TypeError(f"Cannot compare `ConditionComposite` with type {type(other)}")

        return self.conditions_sorted < other.conditions_sorted
