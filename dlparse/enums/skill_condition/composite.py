"""Skill condition composite class."""
from dataclasses import dataclass, field
from typing import Optional, Sequence, Union

from dlparse.enums import Affliction, Element
from dlparse.enums.condition_base import ConditionCompositeBase
from dlparse.errors import ConditionValidationFailedError
from .category import SkillConditionCategories, SkillConditionCheckResult
from .items import SkillCondition
from .validate import validate_skill_conditions

__all__ = ("SkillConditionComposite",)


@dataclass(eq=False)  # ``eq=False`` to keep the superclass ``__hash__``
class SkillConditionComposite(ConditionCompositeBase[SkillCondition]):
    """Composite class of various attacking skill conditions."""

    afflictions_condition: set[SkillCondition] = field(init=False)
    afflictions_converted: set[Affliction] = field(init=False)
    buff_count: Optional[SkillCondition] = field(init=False)
    buff_count_converted: int = field(init=False)
    bullet_hit_count: Optional[SkillCondition] = field(init=False)
    bullet_hit_count_converted: int = field(init=False)
    hp_condition: Optional[SkillCondition] = field(init=False)
    teammate_coverage: Optional[SkillCondition] = field(init=False)
    teammate_coverage_converted: int = field(init=False)
    target_elemental: Optional[SkillCondition] = field(init=False)
    target_elemental_converted: Element = field(init=False)

    @staticmethod
    def _init_validate_conditions(conditions: tuple[SkillCondition]):
        # Validate the condition combinations
        # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
        if not (result := validate_skill_conditions(conditions)):  # pylint: disable=superfluous-parens
            raise ConditionValidationFailedError(result)

    def _init_validate_fields(self, conditions: tuple[SkillCondition]):
        # Check `self.afflictions_condition`
        if any(condition not in SkillConditionCategories.target_affliction
               for condition in self.afflictions_condition):
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_AFFLICTION_ONLY)

        # Check `self.buff_count`
        if self.buff_count and self.buff_count not in SkillConditionCategories.self_buff_count:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_BUFF_COUNT)

        # Check `self.bullet_hit_count`
        if self.bullet_hit_count and self.bullet_hit_count not in SkillConditionCategories.skill_bullet_hit:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_BULLET_HIT_COUNT)

        # Check `self.hp_condition`
        if self.hp_condition and self.hp_condition not in SkillConditionCategories.self_hp:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_HP_CONDITION)

        # Check `self.teammate_coverage`
        if self.teammate_coverage and self.teammate_coverage not in SkillConditionCategories.skill_teammates_covered:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_TEAMMATE_COVERAGE)

        # Check `self.target_elemental`
        if self.target_elemental and self.target_elemental not in SkillConditionCategories.target_elemental:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_TARGET_ELEMENTAL)

        if cond_not_categorized := (set(conditions) - set(self.conditions_sorted)):
            raise ConditionValidationFailedError(SkillConditionCheckResult.HAS_CONDITIONS_LEFT, cond_not_categorized)

    def __post_init__(self, conditions: Optional[Union[Sequence[SkillCondition], SkillCondition]]):
        conditions = self._init_process_conditions(conditions)

        self.afflictions_condition = SkillConditionCategories.target_affliction.extract(conditions)
        self.buff_count = SkillConditionCategories.self_buff_count.extract(conditions)
        self.bullet_hit_count = SkillConditionCategories.skill_bullet_hit.extract(conditions)
        self.hp_condition = SkillConditionCategories.self_hp.extract(conditions)
        self.teammate_coverage = SkillConditionCategories.skill_teammates_covered.extract(conditions)
        self.target_elemental = SkillConditionCategories.target_elemental.extract(conditions)

        self._init_validate_fields(conditions)

        self.afflictions_converted = \
            {SkillConditionCategories.target_affliction.convert(condition) for condition in self.afflictions_condition}
        self.buff_count_converted = \
            self.buff_count and SkillConditionCategories.self_buff_count.convert(self.buff_count)
        self.bullet_hit_count_converted = \
            self.bullet_hit_count and SkillConditionCategories.skill_bullet_hit.convert(self.bullet_hit_count)
        self.teammate_coverage_converted = \
            self.teammate_coverage and SkillConditionCategories.skill_teammates_covered.convert(self.teammate_coverage)
        self.target_elemental_converted = \
            self.target_elemental and SkillConditionCategories.target_elemental.convert(self.target_elemental)

    @property
    def conditions_sorted(self) -> tuple[SkillCondition]:
        """
        Get the sorted conditions as a tuple.

        Conditions will be sorted in the following order:

        - Afflictions
        - Target element
        - HP
        - Buff count
        - Bullet hit count
        - Teammate coverage
        """
        ret: tuple[SkillCondition] = tuple(self.afflictions_condition)

        if self.target_elemental:
            ret += (self.target_elemental,)

        if self.hp_condition:
            ret += (self.hp_condition,)

        if self.buff_count:
            ret += (self.buff_count,)

        if self.bullet_hit_count:
            ret += (self.bullet_hit_count,)

        if self.teammate_coverage:
            ret += (self.teammate_coverage,)

        return ret

    def __iter__(self):
        return iter(self.conditions_sorted)
