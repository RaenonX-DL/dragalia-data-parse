"""Base classes for a skill data."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar, final

from dlparse.enums import Condition, ConditionCategories, ConditionComposite, Element, ElementFlag
from dlparse.model import HitData
from dlparse.mono.asset import ActionConditionAsset, SkillDataEntry

__all__ = ("SkillEntryBase", "SkillDataBase")


@dataclass
class SkillEntryBase(ABC):
    """Base class for a single entry of a skill data."""

    condition_comp: ConditionComposite

    max_level: int


HT = TypeVar("HT", bound=HitData)
ET = TypeVar("ET", bound=SkillEntryBase)


@dataclass
class SkillDataBase(Generic[HT, ET], ABC):
    """Base class for a single skill data."""

    asset_action_cond: ActionConditionAsset

    skill_data_raw: SkillDataEntry

    hit_data_mtx: list[list[HT]]

    possible_conditions: set[ConditionComposite] = field(init=False, default_factory=ConditionComposite)

    @final
    def _init_possible_conditions_base_elems(self):
        cond_elems: list[set[tuple[Condition, ...]]] = []

        # Get all possible pre-conditions if any
        pre_conditions: set[tuple[Condition, ...]] = {
            (hit_data.pre_condition,)
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
            if hit_data.pre_condition
        }
        if pre_conditions:
            if any(any(pre_condition in ConditionCategories.skill_addl_inputs
                       for pre_condition in pre_condition_tuple) for pre_condition_tuple in pre_conditions):
                # Pre-condition has additional inputs condition,
                # no-additional-input (additional input = 0) condition is possible
                # Used to handle Lathna S1 (`105505021`), Ramona S1 (`104501011`)
                pre_conditions.add((Condition.ADDL_INPUT_0,))

            if any(any(pre_condition in ConditionCategories.skill_action_cancel
                       for pre_condition in pre_condition_tuple) for pre_condition_tuple in pre_conditions):
                # Pre-condition has action cancelling condition,
                # no cancelling (no condition) is possible
                # Used to handle Formal Joachim S1 (`109503011`)
                pre_conditions.add(())

            if any(any(pre_condition == Condition.MARK_EXPLODES
                       for pre_condition in pre_condition_tuple) for pre_condition_tuple in pre_conditions):
                # Mark explosion pre-condition, not exploding marks = skill itself
                # Used to handle Nobunaga S1 (`102501031`)
                pre_conditions.add(())

            cond_elems.append(pre_conditions)

        # Get the elemental restriction from the action conditions if any
        action_conds_elem_flag: set[ElementFlag] = set()
        for hit_data_lv in self.hit_data_mtx:
            for hit_data in hit_data_lv:
                if not hit_data.hit_attr.has_action_condition:
                    continue  # No action condition

                action_conds_elem_flag.add(
                    self.asset_action_cond.get_data_by_id(hit_data.hit_attr.action_condition_id).elemental_target
                )
        if action_conds_elem_flag:
            # Elemental action condition available

            # Convert discovered elemental flags to elements
            action_conds_elem: set[Element] = set()
            for elem_flag in action_conds_elem_flag:
                action_conds_elem.update(Element.from_flag(elem_flag))

            # Convert elements to conditions and add it
            # - Dummy condition tuple for pre-condition of none, meaning other elements
            cond_elems.append(
                {(ConditionCategories.target_element.convert_reversed(elem),) for elem in action_conds_elem}
                | {()}
            )

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
    def with_conditions(self, condition_comp: ConditionComposite = None) -> ET:
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
