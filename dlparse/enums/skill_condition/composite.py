"""Skill condition composite class."""
from dataclasses import dataclass, field
from typing import Optional, Sequence, Union

from dlparse.enums.condition_base import ConditionCompositeBase
from dlparse.errors import ConditionValidationFailedError
from .category import SkillConditionCategories as CondCat, SkillConditionCheckResult
from .items import SkillCondition
from .validate import validate_skill_conditions
from ..element import Element
from ..status import Status

__all__ = ("SkillConditionComposite",)


# ``eq=False`` to keep the ``__hash__`` of the superclass
# ``repr=False`` to keep the ``__repr__`` of the superclass
@dataclass(eq=False, repr=False)
class SkillConditionComposite(ConditionCompositeBase[SkillCondition]):
    """Composite class of various attacking skill conditions."""

    # region Target
    afflictions_condition: set[SkillCondition] = field(init=False)
    afflictions_converted: set[Status] = field(init=False)
    target_elemental: Optional[SkillCondition] = field(init=False)
    target_elemental_converted: Element = field(init=False)
    # endregion

    # region Self status
    hp_status: Optional[SkillCondition] = field(init=False)
    hp_status_converted: float = field(init=False)
    hp_condition: Optional[SkillCondition] = field(init=False)
    buff_count: Optional[SkillCondition] = field(init=False)
    buff_count_converted: int = field(init=False)
    buff_zone_self: Optional[SkillCondition] = field(init=False)
    buff_zone_self_converted: int = field(init=False)
    buff_zone_ally: Optional[SkillCondition] = field(init=False)
    buff_zone_ally_converted: int = field(init=False)
    self_action_cond: Optional[SkillCondition] = field(init=False)
    self_action_cond_id: int = field(init=False)
    # endregion

    # region Skill effect / animation
    teammate_coverage: Optional[SkillCondition] = field(init=False)
    teammate_coverage_converted: int = field(init=False)
    bullet_hit_count: Optional[SkillCondition] = field(init=False)
    bullet_hit_count_converted: int = field(init=False)
    bullets_on_map: Optional[SkillCondition] = field(init=False)
    bullets_on_map_converted: int = field(init=False)
    addl_inputs: Optional[SkillCondition] = field(init=False)
    addl_inputs_converted: int = field(init=False)

    # endregion

    @staticmethod
    def _init_validate_conditions(conditions: tuple[SkillCondition]):
        # Validate the condition combinations
        # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
        if not (result := validate_skill_conditions(conditions)):  # pylint: disable=superfluous-parens
            raise ConditionValidationFailedError(result)

    def _init_validate_target(self):
        # Check `self.afflictions_condition`
        if any(condition not in CondCat.target_status
               for condition in self.afflictions_condition):
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_AFFLICTION_ONLY)

        # Check `self.target_elemental`
        if self.target_elemental and self.target_elemental not in CondCat.target_elemental:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_TARGET_ELEMENTAL)

    def _init_validate_self(self):
        # Check `self.hp_status`
        if self.hp_status and self.hp_status not in CondCat.self_hp_status:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_HP_STATUS)

        # Check `self.hp_condition`
        if self.hp_condition and self.hp_condition not in CondCat.self_hp_cond:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_HP_CONDITION)

        # Check `self.buff_count`
        if self.buff_count and self.buff_count not in CondCat.self_buff_count:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_BUFF_COUNT)

        # Check `self.bullet_hit_count`
        if self.bullet_hit_count and self.bullet_hit_count not in CondCat.skill_bullet_hit:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_BULLET_HIT_COUNT)

        # Check `self.buff_zone_self`
        if self.buff_zone_self and self.buff_zone_self not in CondCat.self_in_buff_zone_self:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_BUFF_ZONE_SELF)

        # Check `self.buff_zone_ally`
        if self.buff_zone_ally and self.buff_zone_ally not in CondCat.self_in_buff_zone_ally:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_BUFF_ZONE_ALLY)

        # Check `self.self_action_cond`
        if self.self_action_cond and self.self_action_cond not in CondCat.self_action_condition:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_SELF_ACTION_CONDITION)

    def _init_validate_skill(self):
        # Check `self.teammate_coverage`
        if self.teammate_coverage and self.teammate_coverage not in CondCat.skill_teammates_covered:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_TEAMMATE_COVERAGE)

        # Check `self.bullet_hit_count`
        if self.bullet_hit_count and self.bullet_hit_count not in CondCat.skill_bullet_hit:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_BULLET_HIT_COUNT)

        # Check `self.bullets_on_map`
        if self.bullets_on_map and self.bullets_on_map not in CondCat.skill_bullets_on_map:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_BULLETS_ON_MAP)

        # Check `self.addl_inputs`
        if self.addl_inputs and self.addl_inputs not in CondCat.skill_addl_inputs:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_ADDL_INPUTS)

    def _init_validate_fields(self, conditions: tuple[SkillCondition]):
        self._init_validate_target()
        self._init_validate_self()
        self._init_validate_skill()

        if cond_not_categorized := (set(conditions) - set(self.conditions_sorted)):
            raise ConditionValidationFailedError(SkillConditionCheckResult.HAS_CONDITIONS_LEFT, cond_not_categorized)

    def __post_init__(self, conditions: Optional[Union[Sequence[SkillCondition], SkillCondition]]):
        conditions = self._init_process_conditions(conditions)

        self.afflictions_condition = CondCat.target_status.extract(conditions)
        self.target_elemental = CondCat.target_elemental.extract(conditions)

        self.hp_status = CondCat.self_hp_status.extract(conditions)
        self.hp_condition = CondCat.self_hp_cond.extract(conditions)
        self.buff_count = CondCat.self_buff_count.extract(conditions)
        self.buff_zone_self = CondCat.self_in_buff_zone_self.extract(conditions)
        self.buff_zone_ally = CondCat.self_in_buff_zone_ally.extract(conditions)
        self.self_action_cond = CondCat.self_action_condition.extract(conditions)

        self.teammate_coverage = CondCat.skill_teammates_covered.extract(conditions)
        self.bullet_hit_count = CondCat.skill_bullet_hit.extract(conditions)
        self.bullets_on_map = CondCat.skill_bullets_on_map.extract(conditions)
        self.addl_inputs = CondCat.skill_addl_inputs.extract(conditions)

        self._init_validate_fields(conditions)

        self.afflictions_converted = {
            CondCat.target_status.convert(condition) for condition in self.afflictions_condition
        }
        self.target_elemental_converted = CondCat.target_elemental.convert(self.target_elemental, on_missing=None)

        self.hp_status_converted = CondCat.self_hp_status.convert(self.hp_status, on_missing=1)
        self.buff_count_converted = CondCat.self_buff_count.convert(self.buff_count, on_missing=None)
        self.buff_zone_self_converted = CondCat.self_in_buff_zone_self.convert(self.buff_zone_self, on_missing=None)
        self.buff_zone_ally_converted = CondCat.self_in_buff_zone_ally.convert(self.buff_zone_ally, on_missing=None)
        self.self_action_cond_id = CondCat.self_action_condition.convert(self.self_action_cond, on_missing=None)

        self.teammate_coverage_converted = CondCat.skill_teammates_covered.convert(self.teammate_coverage,
                                                                                   on_missing=None)
        self.bullet_hit_count_converted = CondCat.skill_bullet_hit.convert(self.bullet_hit_count, on_missing=None)
        self.bullets_on_map_converted = CondCat.skill_bullets_on_map.convert(self.bullets_on_map, on_missing=None)
        self.addl_inputs_converted = CondCat.skill_addl_inputs.convert(self.addl_inputs, on_missing=None)

    def _cond_sorted_target(self) -> tuple[SkillCondition]:
        ret: tuple[SkillCondition] = tuple(self.afflictions_condition)

        if self.target_elemental:
            ret += (self.target_elemental,)

        return ret

    def _cond_sorted_self_status(self) -> tuple[SkillCondition]:
        ret: tuple[SkillCondition] = tuple()

        if self.hp_status:
            ret += (self.hp_status,)

        if self.hp_condition:
            ret += (self.hp_condition,)

        if self.buff_count:
            ret += (self.buff_count,)

        if self.buff_zone_self:
            ret += (self.buff_zone_self,)

        if self.buff_zone_ally:
            ret += (self.buff_zone_ally,)

        if self.self_action_cond:
            ret += (self.self_action_cond,)

        return ret

    def _cond_sorted_skill(self) -> tuple[SkillCondition]:
        ret: tuple[SkillCondition] = tuple()

        if self.bullet_hit_count:
            ret += (self.bullet_hit_count,)

        if self.teammate_coverage:
            ret += (self.teammate_coverage,)

        if self.bullets_on_map:
            ret += (self.bullets_on_map,)

        if self.addl_inputs:
            ret += (self.addl_inputs,)

        return ret

    @property
    def conditions_sorted(self) -> tuple[SkillCondition, ...]:
        """
        Get the sorted conditions as a tuple.

        Conditions will be sorted in the following order:

        - [Target] Afflictions
        - [Target] Target element
        - [Self] HP status / condition
        - [Self] Buff count
        - [Self] Buff zone built by self / ally
        - [Self] Self action condition
        - [Skill] Bullet hit count
        - [Skill] Teammate coverage
        - [Skill] Bullets on map
        - [Skill] Additional inputs
        """
        return (self._cond_sorted_target()
                + self._cond_sorted_self_status()
                + self._cond_sorted_skill())

    def __iter__(self):
        return iter(self.conditions_sorted)

    def __add__(self, other):
        if not isinstance(other, SkillConditionComposite):
            raise TypeError(f"Cannot add `SkillConditionComposite` with type {type(other)}")

        return SkillConditionComposite(self.conditions_sorted + other.conditions_sorted)

    def __lt__(self, other):
        if not isinstance(other, SkillConditionComposite):
            raise TypeError(f"Cannot compare `SkillConditionComposite` with type {type(other)}")

        return self.conditions_sorted < other.conditions_sorted
