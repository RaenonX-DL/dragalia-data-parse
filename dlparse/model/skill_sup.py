"""Class for a single supportive skill entry."""
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import product
from typing import Optional

from dlparse.enums import Condition, ConditionCategories, ConditionComposite, Element
from dlparse.errors import MultipleActionsError
from dlparse.mono.asset import ActionConditionAsset
from .action_cond_effect import HitActionConditionEffectUnit
from .base import SkillDataBase, SkillEntryBase
from .hit_buff import BuffingHitData

__all__ = ("SupportiveSkillEntry", "SupportiveSkillData")


@dataclass
class SupportiveSkillEntry(SkillEntryBase):
    """
    A single entry for a supportive skill. This contains all buffs across all levels under a certain condition.

    To get the buffs at a certain level, use ``self.buffs[skill_lv - 1]``.
    """

    buffs: list[set[HitActionConditionEffectUnit]]

    max_level: int = field(init=False)

    def __post_init__(self):
        self.max_level = len(self.buffs)

    @property
    def max_lv_buffs(self) -> set[HitActionConditionEffectUnit]:
        """Get the buffs at the max level."""
        return self.buffs[-1]


@dataclass
class SupportiveSkillData(SkillDataBase[BuffingHitData, SupportiveSkillEntry]):
    """
    A supportive skill data.

    All buffs can be generated from this class as :class:`SupportiveSkillEntry`. Each entry contains exactly one buff.
    """

    buffs_base: list[set[HitActionConditionEffectUnit]] = field(init=False)
    """
    Base buffs. These buffs will be granted without any additional conditions.

    Calling ``buffs_base[skill_lv]`` will return a set of buffs at ``skill_lv``.
    """
    buffs_elemental: list[dict[Element, set[HitActionConditionEffectUnit]]] = field(init=False)
    """
    Buffs to be granted only if the target element matches.

    Calling ``buffs_elemental[skill_lv][element_enum]`` will return a set of buffs at ``skill_lv``
    when the target element is ``element_enum``.
    """
    buffs_pre_conditioned: list[dict[ConditionComposite, set[HitActionConditionEffectUnit]]] = field(init=False)
    """
    Buffs to be granted only if the condition matches.

    Calling ``buffs_hp_condition[skill_lv][condition]`` will return a set of buffs at ``skill_lv``
    when the target condition matches ``condition``.
    """

    def _init_all_possible_conditions(self, action_condition_asset: ActionConditionAsset):
        # Check availabilities
        has_teammate_coverage: bool = any(
            hit_data.hit_attr.has_hit_condition
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        # noinspection PyUnboundLocalVariable
        has_elemental_restriction: bool = any(
            action_cond.target_limited_by_element
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
            if (hit_data.hit_attr.has_action_condition
                and (action_cond := action_condition_asset.get_data_by_id(hit_data.action_condition_id)))
        )

        # Initialization
        cond_elems: list[set[tuple[Condition, ...]]] = self._init_possible_conditions_base_elems()

        # Teammate coverage conditions available
        if has_teammate_coverage:
            cond_elems.append({(teammate_coverage_cond,) for teammate_coverage_cond
                               in ConditionCategories.skill_teammates_covered.members})

        # Elemental restriction available
        if has_elemental_restriction:
            cond_elems.append({
                (target_element_cond,)
                for target_element_cond in ConditionCategories.target_element.members
                if any(
                    buffs_lv[ConditionCategories.target_element.convert(target_element_cond)]
                    for buffs_lv in self.buffs_elemental
                )
            })

        # Add combinations
        self.possible_conditions = {
            ConditionComposite(tuple(subitem for item in item_combination for subitem in item))
            for item_combination in product(*cond_elems)
        }

    def _init_base_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_base = []

        for hit_data_lv in self.skill_hit_data.hit_data:
            buff_lv = set()

            for hit_data in hit_data_lv:
                if hit_data.hit_attr.has_hit_condition:
                    # Skip conditions that require teammate coverage, let ``buffs_teammate_coverage`` handles this
                    continue

                if hit_data.hit_attr.has_action_condition:
                    action_condition = action_condition_asset.get_data_by_id(hit_data.action_condition_id)
                    if action_condition.target_limited_by_element:
                        # Skip conditions that require certain elements, let ``buffs_elemental`` handles this
                        continue

                if hit_data.pre_condition_comp:
                    # Skip conditions that has pre condition, let ``buffs_pre_conditioned`` handles this
                    continue

                buff_lv.update(hit_data.to_buffing_units(action_condition_asset))

            self.buffs_base.append(buff_lv)

    def _init_elemental_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_elemental: list[dict[Element, set[HitActionConditionEffectUnit]]] = []

        for hit_data_lv in self.skill_hit_data.hit_data:
            buff_lv: dict[Element, set[HitActionConditionEffectUnit]] = {
                elem: set() for elem in Element.get_all_valid_elements()
            }

            for hit_data in hit_data_lv:
                if not hit_data.hit_attr.has_action_condition:
                    continue  # No action condition assigned

                action_condition = action_condition_asset.get_data_by_id(hit_data.action_condition_id)

                if not action_condition.target_limited_by_element:
                    continue  # Action condition not limited by element

                for elem in action_condition.elemental_target.elements:
                    buff_lv[elem].update(hit_data.to_buffing_units(action_condition_asset))

            self.buffs_elemental.append(buff_lv)

    def _init_pre_conditioned_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_pre_conditioned = []

        for hit_data_lv in self.skill_hit_data.hit_data:
            buff_lv: dict[ConditionComposite, set[HitActionConditionEffectUnit]] = defaultdict(set)

            for hit_data in hit_data_lv:
                if not hit_data.pre_condition_comp:
                    # Skip adding the hit data that does not have pre-condition
                    continue

                buff_lv[hit_data.pre_condition_comp].update(hit_data.to_buffing_units(action_condition_asset))

            self.buffs_pre_conditioned.append(dict(buff_lv))

    def __post_init__(self):
        self._init_base_buffs(self.asset_manager.asset_action_cond)
        self._init_elemental_buffs(self.asset_manager.asset_action_cond)
        self._init_pre_conditioned_buffs(self.asset_manager.asset_action_cond)

        # Fields need to be initialized first to get all possible preconditions
        super().__post_init__(self.asset_manager.asset_action_cond)

    def _teammate_coverage_effects(
            self, condition_comp: ConditionComposite, action_id: Optional[int]
    ) -> list[list[set[HitActionConditionEffectUnit]]]:
        """
        Get the effects to grant for different count of teammates covered.

        If there are multiple actions sharing the same condition, ``action_id`` must be specified.
        Otherwise, :class:`MultipleActionsError` will be raised.

        Calling ``buffs_teammate_coverage[skill_lv][teammate_count]`` will return a set of buffs at ``skill_lv``
        when ``teammate_count`` covered.

        :raises MultipleActionsError: if there are multiple actions sharing the same condition
        """
        ret = []
        action_id_mtx: list[set[int]] = []

        teammate_coverage_counts = ConditionCategories.skill_teammates_covered.targets

        for hit_count, hit_data_lv in zip(self.skill_hit_data.hit_count, self.hit_data_mtx):
            buff_lv: list[set[HitActionConditionEffectUnit]] = [set() for _ in teammate_coverage_counts]
            new_action_ids_level: set[int] = set()

            if not any(hit_data.hit_attr.has_hit_condition for hit_data in hit_data_lv):
                ret.append(buff_lv)
                continue  # No skill hit condition

            for hit_data in hit_data_lv:
                if action_id and action_id != hit_data.action_id:
                    continue  # Skip processing if the action ID of `hit_data` is not the desired one

                hit_attr = hit_data.hit_attr

                # Non-dummy hit count already counted as ``hit_count``
                # (counted when getting the skill hit data in skill transformer),
                # therefore only counting dummy hit counts here.
                if hit_attr.dummy_hit_count:
                    hit_count += hit_data.get_hit_count(hit_count, condition_comp, self.asset_manager)

                for teammate_count in teammate_coverage_counts:
                    if not hit_attr.has_hit_condition:
                        continue  # No skill hit condition
                    if not hit_attr.is_effective_hit_count(hit_count):
                        continue  # Hit attribute ineffective

                    buff_lv[teammate_count].update(hit_data.to_buffing_units(self.asset_manager.asset_action_cond))

                new_action_ids_level.add(hit_data.action_id)

            action_id_mtx.append(new_action_ids_level)
            ret.append(buff_lv)

        if any(len(action_ids_level) > 1 for action_ids_level in action_id_mtx):
            raise MultipleActionsError(action_id_mtx)

        return ret

    def with_conditions(
            self, condition_comp: Optional[ConditionComposite] = None, *, action_id: Optional[int] = None
    ) -> SupportiveSkillEntry:
        if not condition_comp:
            condition_comp = ConditionComposite()  # Dummy empty condition composite

        # Deep copy buff base
        buffs: list[set[HitActionConditionEffectUnit]] = [buff_set.copy() for buff_set in self.buffs_base]

        # Attach teammate coverage only buffs
        if condition_comp.teammate_coverage:
            coverage_effects = self._teammate_coverage_effects(condition_comp, action_id)

            for skill_lv in range(self.max_level):
                buffs[skill_lv].update(coverage_effects[skill_lv][condition_comp.teammate_coverage_converted])

        # Attach elemental buffs
        if condition_comp.target_element:
            for skill_lv in range(self.max_level):
                buffs[skill_lv].update(self.buffs_elemental[skill_lv][condition_comp.target_element_converted])

        # Attach pre-conditioned buffs, if matches
        for skill_lv in range(self.max_level):
            for pre_cond, effect_units in self.buffs_pre_conditioned[skill_lv].items():
                if pre_cond not in condition_comp:
                    continue

                buffs[skill_lv].update(effect_units)

        return SupportiveSkillEntry(condition_comp=condition_comp, buffs=buffs)

    @property
    def max_level(self) -> int:
        """
        Get the max level of the skill.

        This is **NOT** the actual in-game max level.
        """
        return len(self.hit_data_mtx)
