"""Base classes for a skill data."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TYPE_CHECKING, TypeVar, final

from dlparse.enums import Condition, ConditionCategories, ConditionComposite, Element, ElementFlag
from dlparse.mono.asset import SkillDataEntry
from .hit import HitData

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager
    from dlparse.transformer import SkillHitData

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

    asset_manager: "AssetManager"

    skill_hit_data: "SkillHitData"

    skill_data: SkillDataEntry = field(init=False)
    hit_data_mtx: list[list[HT]] = field(init=False)

    possible_conditions: set[ConditionComposite] = field(init=False, default_factory=ConditionComposite)

    @final
    def _init_possible_conditions_base_elems(self):
        cond_elems: list[set[tuple[Condition, ...]]] = []

        # Get all possible pre-conditions
        pre_conditions: set[tuple[Condition, ...]] = {
            tuple(hit_data.pre_condition_comp)
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
            if hit_data.pre_condition_comp
        }
        if pre_conditions:
            if any(any(pre_condition in ConditionCategories.skill_addl_inputs
                       for pre_condition in pre_condition_tuple) for pre_condition_tuple in pre_conditions):
                # Pre-condition has additional inputs condition,
                # no-additional-input (additional input = 0) condition is possible
                # Appears in Lathna S1 (`105505021`), Ramona S1 (`104501011`)
                pre_conditions.add((Condition.ADDL_INPUT_0,))

            if any(any(pre_condition in ConditionCategories.skill_action_cancel
                       for pre_condition in pre_condition_tuple) for pre_condition_tuple in pre_conditions):
                # Pre-condition has action cancelling condition,
                # no cancelling (no condition) is possible
                # Appears in handle Formal Joachim S1 (`109503011`)
                pre_conditions.add(())

            if any(any(pre_condition in ConditionCategories.skill_action_misc_var
                       for pre_condition in pre_condition_tuple) for pre_condition_tuple in pre_conditions):
                # Skill has some variants. However, the skill can be used without triggering the variants.
                # Appears in Nobunaga S1 (`102501031`), Yoshitsune S1 (`109502021`)
                pre_conditions.add(())

            cond_elems.append(pre_conditions)

        # Get the elemental restriction from the action conditions if any
        action_conds_elem_flag: set[ElementFlag] = set()
        for hit_data_lv in self.hit_data_mtx:
            for hit_data in hit_data_lv:
                if not hit_data.action_condition_id:
                    continue  # No action condition

                action_conds_elem_flag.add(
                    self.asset_manager.asset_action_cond.get_data_by_id(hit_data.action_condition_id).elemental_target
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
        self.skill_data = self.skill_hit_data.skill_data
        self.hit_data_mtx = self.skill_hit_data.hit_data

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
