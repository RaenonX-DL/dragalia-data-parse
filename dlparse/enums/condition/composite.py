"""Condition composite class."""
from dataclasses import dataclass, field
from typing import ClassVar, Iterable, Optional, TYPE_CHECKING, Union

from dlparse.enums.condition_base import ConditionCompositeBase
from dlparse.errors import ConditionValidationFailedError
from .category import ConditionCategories as CondCat, ConditionCheckResult
from .items import Condition
from .validate import validate_conditions
from ..element import Element
from ..status import Status

if TYPE_CHECKING:
    from dlparse.mono.asset import BuffCountAsset, HitAttrEntry

__all__ = ("ConditionComposite",)


# ``eq=False`` to keep the ``__hash__`` of the superclass
# ``repr=False`` to keep the ``__repr__`` of the superclass
@dataclass(eq=False, repr=False)
class ConditionComposite(ConditionCompositeBase[Condition]):
    """Composite class of various attacking conditions."""

    allowed_not_categorize_conds: ClassVar[set[Condition]] = {
        # Target state
        Condition.TARGET_OD_STATE,
        Condition.TARGET_BK_STATE,
        # Special self status
        Condition.SELF_ENERGIZED,
        Condition.SELF_SHAPESHIFTED,
        Condition.SELF_SHAPESHIFT_COMPLETED,
        # Upon skill usage
        Condition.SKILL_USED_S1,
        Condition.SKILL_USED_S2,
        Condition.SKILL_USED_ALL,
        # Misc
        Condition.MARK_EXPLODES,
        Condition.COUNTER_RED_ATTACK,
        Condition.QUEST_START
    }

    # region Target
    afflictions_condition: set[Condition] = field(init=False)
    afflictions_converted: set[Status] = field(init=False)
    target_element: Optional[Condition] = field(init=False)
    target_element_converted: Element = field(init=False)
    target_in_od: bool = field(init=False)
    target_in_bk: bool = field(init=False)
    # endregion

    # region Self status
    hp_status: Optional[Condition] = field(init=False)
    hp_status_converted: float = field(init=False)
    hp_condition: Optional[Condition] = field(init=False)
    combo_count: Optional[Condition] = field(init=False)
    combo_count_converted: int = field(init=False)
    buff_count: Optional[Condition] = field(init=False)
    buff_count_converted: int = field(init=False)
    buff_zone_self: Optional[Condition] = field(init=False)
    buff_zone_self_converted: int = field(init=False)
    buff_zone_ally: Optional[Condition] = field(init=False)
    buff_zone_ally_converted: int = field(init=False)
    action_cond: Optional[Condition] = field(init=False)
    action_cond_id: int = field(init=False)
    gauge_filled: Optional[Condition] = field(init=False)
    gauge_filled_converted: int = field(init=False)
    is_shapeshifted: bool = field(init=False)
    shapeshift_count: Optional[Condition] = field(init=False)
    shapeshift_count_converted: int = field(init=False)
    # endregion

    # region Skill effect / animation
    teammate_coverage: Optional[Condition] = field(init=False)
    teammate_coverage_converted: int = field(init=False)
    bullet_hit_count: Optional[Condition] = field(init=False)
    bullet_hit_count_converted: int = field(init=False)
    bullets_on_map: Optional[Condition] = field(init=False)
    bullets_on_map_converted: int = field(init=False)
    addl_inputs: Optional[Condition] = field(init=False)
    addl_inputs_converted: int = field(init=False)
    action_cancel: Optional[Condition] = field(init=False)
    action_counter: bool = field(init=False)
    mark_explode: bool = field(init=False)
    # endregion

    # region Other fields
    trigger: Condition = field(init=False)
    # endregion

    # region Other fields (hidden)
    _has_buff_boost_condition: bool = field(init=False)

    # endregion

    @staticmethod
    def _init_validate_conditions(conditions: tuple[Condition]):
        # Validate the condition combinations
        # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
        if not (result := validate_conditions(conditions)):  # pylint: disable=superfluous-parens
            raise ConditionValidationFailedError(result)

    def _init_validate_target(self):
        # Check `self.afflictions_condition`
        if any(condition not in CondCat.target_status
               for condition in self.afflictions_condition):
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_AFFLICTION_ONLY)

        # Check `self.target_element`
        if self.target_element and self.target_element not in CondCat.target_element:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_TARGET_ELEMENTAL)

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

        # Check `self.buff_zone_self`
        if self.buff_zone_self and self.buff_zone_self not in CondCat.self_in_buff_zone_self:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_BUFF_ZONE_SELF)

        # Check `self.buff_zone_ally`
        if self.buff_zone_ally and self.buff_zone_ally not in CondCat.self_in_buff_zone_ally:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_BUFF_ZONE_ALLY)

    def _init_validate_self_special(self):
        # Check `self.action_cond`
        if self.action_cond and self.action_cond not in CondCat.action_condition:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_ACTION_CONDITION)

        # Check `self.gauge_filled`
        if self.gauge_filled and self.gauge_filled not in CondCat.self_gauge_filled:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_GAUGE_FILLED)

        # Check `self.shapeshift_count`
        if not self.is_shapeshifted and self.shapeshift_count:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_SHAPESHIFT_NOT_SET)
        if self.shapeshift_count and self.shapeshift_count not in CondCat.shapeshifted_count:
            raise ConditionValidationFailedError(ConditionCheckResult.INTERNAL_NOT_SHAPESHIFT_COUNT)

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

    def _init_validate_fields(self, conditions: tuple[Condition]):
        self._init_validate_target()
        self._init_validate_self_general()
        self._init_validate_self_special()
        self._init_validate_skill()
        self._init_validate_others()

        if cond_not_categorized := (set(conditions) - set(self.conditions_sorted) - self.allowed_not_categorize_conds):
            raise ConditionValidationFailedError(ConditionCheckResult.HAS_CONDITIONS_LEFT, cond_not_categorized)

    def __post_init__(self, conditions: Optional[Union[Iterable[Condition], Condition]]):
        conditions = self._init_process_conditions(conditions)

        # region Categorized condition fields
        self.afflictions_condition = CondCat.target_status.extract(conditions)
        self.target_element = CondCat.target_element.extract(conditions)
        self.target_in_od = Condition.TARGET_OD_STATE in conditions
        self.target_in_bk = Condition.TARGET_BK_STATE in conditions

        self.hp_status = CondCat.self_hp_status.extract(conditions)
        self.hp_condition = CondCat.self_hp_cond.extract(conditions)
        self.combo_count = CondCat.self_combo_count.extract(conditions)
        self.buff_count = CondCat.self_buff_count.extract(conditions)
        self.buff_zone_self = CondCat.self_in_buff_zone_self.extract(conditions)
        self.buff_zone_ally = CondCat.self_in_buff_zone_ally.extract(conditions)
        self.action_cond = CondCat.action_condition.extract(conditions)
        self.gauge_filled = CondCat.self_gauge_filled.extract(conditions)
        self.shapeshift_count = CondCat.shapeshifted_count.extract(conditions)
        self.is_shapeshifted = Condition.SELF_SHAPESHIFTED in conditions or self.shapeshift_count

        self.teammate_coverage = CondCat.skill_teammates_covered.extract(conditions)
        self.bullet_hit_count = CondCat.skill_bullet_hit.extract(conditions)
        self.bullets_on_map = CondCat.skill_bullets_on_map.extract(conditions)
        self.addl_inputs = CondCat.skill_addl_inputs.extract(conditions)
        self.action_cancel = CondCat.skill_action_cancel.extract(conditions)
        self.action_counter = Condition.COUNTER_RED_ATTACK in conditions
        self.mark_explode = Condition.MARK_EXPLODES in conditions

        self.trigger = CondCat.trigger.extract(conditions)
        # endregion

        self._init_validate_fields(conditions)

        # region Converted fields
        self.afflictions_converted = {
            CondCat.target_status.convert(condition) for condition in self.afflictions_condition
        }
        self.target_element_converted = CondCat.target_element.convert(self.target_element, on_missing=None)

        self.hp_status_converted = CondCat.self_hp_status.convert(self.hp_status, on_missing=1)
        self.combo_count_converted = CondCat.self_combo_count.convert(self.combo_count, on_missing=0)
        self.buff_count_converted = CondCat.self_buff_count.convert(self.buff_count, on_missing=0)
        self.buff_zone_self_converted = CondCat.self_in_buff_zone_self.convert(self.buff_zone_self, on_missing=0)
        self.buff_zone_ally_converted = CondCat.self_in_buff_zone_ally.convert(self.buff_zone_ally, on_missing=0)
        self.action_cond_id = CondCat.action_condition.convert(self.action_cond, on_missing=None)
        self.gauge_filled_converted = CondCat.self_gauge_filled.convert(self.gauge_filled, on_missing=0)
        self.shapeshift_count_converted = CondCat.shapeshifted_count.convert(self.shapeshift_count, on_missing=0)

        self.teammate_coverage_converted = CondCat.skill_teammates_covered.convert(self.teammate_coverage,
                                                                                   on_missing=None)
        self.bullet_hit_count_converted = CondCat.skill_bullet_hit.convert(self.bullet_hit_count, on_missing=None)
        self.bullets_on_map_converted = CondCat.skill_bullets_on_map.convert(self.bullets_on_map, on_missing=None)
        self.addl_inputs_converted = CondCat.skill_addl_inputs.convert(self.addl_inputs, on_missing=None)
        # endregion

        # region Other fields
        self._has_buff_boost_condition = any(
            condition in CondCat.self_buff_count or condition in CondCat.self_lapis_card
            for condition in conditions
        )
        # endregion

    def _cond_sorted_target(self) -> tuple[Condition]:
        ret: tuple[Condition] = tuple(self.afflictions_condition)

        if self.target_element:
            ret += (self.target_element,)

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

        if self.buff_zone_self:
            ret += (self.buff_zone_self,)

        if self.buff_zone_ally:
            ret += (self.buff_zone_ally,)

        return ret

    def _cond_sorted_self_special(self) -> tuple[Condition]:
        ret: tuple[Condition] = tuple()

        if self.action_cond:
            ret += (self.action_cond,)

        if self.gauge_filled:
            ret += (self.gauge_filled,)

        if self.is_shapeshifted:
            ret += (Condition.SELF_SHAPESHIFTED,)

        if self.shapeshift_count:
            ret += (self.shapeshift_count,)

        return ret

    def _cond_sorted_skill(self) -> tuple[Condition]:
        ret: tuple[Condition] = tuple()

        if self.bullet_hit_count:
            ret += (self.bullet_hit_count,)

        if self.teammate_coverage:
            ret += (self.teammate_coverage,)

        if self.bullets_on_map:
            ret += (self.bullets_on_map,)

        if self.addl_inputs:
            ret += (self.addl_inputs,)

        if self.action_cancel:
            ret += (self.action_cancel,)

        if self.action_counter:
            ret += (Condition.COUNTER_RED_ATTACK,)

        if self.mark_explode:
            ret += (Condition.MARK_EXPLODES,)

        return ret

    def _cond_sorted_others(self) -> tuple[Condition]:
        ret: tuple[Condition] = tuple()

        if self.trigger:
            ret += (self.trigger,)

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
        - [Self] Buff zone built by self / ally
        - [Self] Self action condition
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
        """
        return (self._cond_sorted_target()
                + self._cond_sorted_self_general()
                + self._cond_sorted_self_special()
                + self._cond_sorted_skill()
                + self._cond_sorted_others())

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

    def __add__(self, other):
        if other is None:
            return self

        if not isinstance(other, ConditionComposite):
            raise TypeError(f"Cannot add `ConditionComposite` with type {type(other)}")

        return ConditionComposite(self.conditions_sorted + other.conditions_sorted)

    def __lt__(self, other):
        if not isinstance(other, ConditionComposite):
            raise TypeError(f"Cannot compare `ConditionComposite` with type {type(other)}")

        return self.conditions_sorted < other.conditions_sorted
