"""Base classes for a skill data."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, Optional, TYPE_CHECKING, TypeVar, final

from dlparse.enums import Condition, ConditionCategories, ConditionComposite, Element, ElementFlag
from dlparse.errors import MultipleActionsError
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
    sp_gradual_fill_pct: list[float] = field(init=False)

    possible_conditions: set[ConditionComposite] = field(init=False, default_factory=ConditionComposite)

    max_level: int = field(init=False)

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

    @final
    def _init_sp_gradual_fill_pct(self):
        gradual_fill_pcts = []
        ability_ids = self.skill_data.ability_id_by_level

        for skill_level in range(self.max_level):
            ability_id = ability_ids[skill_level]
            if not ability_id:
                # No related ability
                gradual_fill_pcts.append(0)
                continue

            root_ability_data = self.asset_manager.asset_ability_data.get_data_by_id(ability_id)
            action_conds = [
                self.asset_manager.asset_action_cond.get_data_by_id(action_condition_id)
                for ability_data in root_ability_data.get_all_ability(self.asset_manager.asset_ability_data).values()
                for action_condition_id in ability_data.action_conditions
            ]
            gradual_fill_pcts.append(sum(action_cond.regen_sp_pct for action_cond in action_conds))

        self.sp_gradual_fill_pct = gradual_fill_pcts

    @abstractmethod
    def _init_max_level(self, *args, **kwargs):
        """Get the maximum skill level and set it to ``self.max_level``."""
        raise NotImplementedError()

    @abstractmethod
    def _init_all_possible_conditions(self, *args, **kwargs):
        """Find all possible conditions and set it to ``self.possible_conditions``."""
        raise NotImplementedError()

    def __post_init__(self, *args, **kwargs):
        self.skill_data = self.skill_hit_data.skill_data
        self.hit_data_mtx = self.skill_hit_data.hit_data

        self.max_level = self._init_max_level()  # Needs to be placed before `self._init_sp_gradual_fill_pct()`
        self._init_all_possible_conditions(*args, **kwargs)
        self._init_sp_gradual_fill_pct()

    def get_all_possible_entries(self) -> list[ET]:
        """Get all possible skill mod entries."""
        entries = []

        for conditions in sorted(self.possible_conditions):
            try:
                entries.append(self.with_conditions(conditions))
            except MultipleActionsError as ex:
                entries.extend([
                    self.with_conditions(conditions, action_id=action_id)
                    for action_id in ex.all_possible_action_ids
                ])

        return entries

    def check_unchained_action_ids_at_same_level(self, action_id_mtx: list[set[int]]):
        """
        Check if there are unchained action IDs occur at the same level.

        :raises MultipleActionsError: if there are unchained action IDs at the same level
        """
        for action_ids_level in action_id_mtx:
            if len(action_ids_level) <= 1:
                continue  # Continue if there is only a single or no action ID at the current level

            parent_action_id = next(iter(sorted(action_ids_level)))
            action_id_chain = self.asset_manager.asset_action_info_player.get_action_id_chain(parent_action_id)

            if action_ids_level.difference(action_id_chain):
                raise MultipleActionsError(action_id_mtx)

    @abstractmethod
    def with_conditions(self, condition_comp: ConditionComposite = None, *, action_id: Optional[int] = None) -> ET:
        """
        Get the skill data when all conditions in ``condition_comp`` hold.

        If there are multiple actions sharing the same condition, ``action_id`` must be specified.
        Otherwise, :class:`MultipleActionsError` will be raised.

        :raises ConditionValidationFailedError: if the condition combination is invalid
        :raises MultipleActionsError: if there are multiple actions sharing the same condition
        """
        raise NotImplementedError()
