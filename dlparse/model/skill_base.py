"""Base classes for a skill data."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar, final

from dlparse.enums import SkillCondition, SkillConditionCategories, SkillConditionComposite
from dlparse.model import HitData
from dlparse.mono.asset import SkillDataEntry

__all__ = ("SkillEntryBase", "SkillDataBase")


@dataclass
class SkillEntryBase(ABC):
    """Base class for a single entry of a skill data."""

    condition_comp: SkillConditionComposite

    max_level: int


HT = TypeVar("HT", bound=HitData)
ET = TypeVar("ET", bound=SkillEntryBase)


@dataclass
class SkillDataBase(Generic[HT, ET], ABC):
    """Base class for a single skill data."""

    skill_data_raw: SkillDataEntry

    hit_data_mtx: list[list[HT]]

    possible_conditions: set[SkillConditionComposite] = field(init=False, default_factory=SkillConditionComposite)

    @final
    def _init_possible_conditions_base_elems(self):
        cond_elems: list[set[tuple[SkillCondition, ...]]] = []

        # Get all possible pre-conditions if any
        pre_conditions: set[tuple[SkillCondition, ...]] = {
            (hit_data.pre_condition,)
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
            if hit_data.pre_condition
        }
        if pre_conditions:
            if any(pre_condition in SkillConditionCategories.skill_addl_inputs
                   for pre_condition_tuple in pre_conditions for pre_condition in pre_condition_tuple):
                # Pre-condition has additional inputs condition,
                # no-additional-input (additional input = 0) condition is possible
                pre_conditions.add((SkillCondition.ADDL_INPUT_0,))

            if any(pre_condition in SkillConditionCategories.skill_action_cancel
                   for pre_condition_tuple in pre_conditions for pre_condition in pre_condition_tuple):
                # Pre-condition has action cancelling condition,
                # no cancelling (no condition) is possible
                pre_conditions.add(())

            cond_elems.append(pre_conditions)

        return cond_elems

    @abstractmethod
    def _init_all_possible_conditions(self, *args, **kwargs):
        """Find all possible conditions and set it to ``self.possible_conditions``."""
        raise NotImplementedError()

    def __post_init__(self, *args, **kwargs):
        self._init_all_possible_conditions(*args, **kwargs)

    def get_all_possible_entries(self) -> list[ET]:
        """Get all possible skill mod entries."""
        entries = []

        for conditions in sorted(self.possible_conditions):
            entries.append(self.with_conditions(conditions))

        return entries

    @abstractmethod
    def with_conditions(self, condition_comp: SkillConditionComposite = None) -> ET:
        """
        Get the skill data when all conditions in ``condition_comp`` hold.

        :raises ConditionValidationFailedError: if the condition combination is invalid
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def max_level(self) -> int:
        """Get the max level of the skill."""
        raise NotImplementedError()
