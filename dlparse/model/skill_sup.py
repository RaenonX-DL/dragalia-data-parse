"""Class for a single supportive skill entry."""
from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from itertools import product
from typing import Optional

from dlparse.enums import Element, SkillCondition, SkillConditionCategories, SkillConditionComposite
from dlparse.mono.asset import ActionConditionAsset
from .effect_action_cond import ActionConditionEffectUnit
from .hit_buff import BuffingHitData
from .skill_base import SkillDataBase, SkillEntryBase

__all__ = ("SupportiveSkillEntry", "SupportiveSkillData")


@dataclass
class SupportiveSkillEntry(SkillEntryBase):
    """
    A single entry for a supportive skill. This contains all buffs across all levels under a certain condition.

    To get the buffs at a certain level, use ``self.buffs[skill_lv - 1]``.
    """

    buffs: list[set[ActionConditionEffectUnit]]

    max_level: int = field(init=False)

    def __post_init__(self):
        self.max_level = len(self.buffs)

    @property
    def max_lv_buffs(self) -> set[ActionConditionEffectUnit]:
        """Get the buffs at the max level."""
        return self.buffs[-1]


@dataclass
class SupportiveSkillData(SkillDataBase[BuffingHitData, SupportiveSkillEntry]):
    """
    A supportive skill data.

    All buffs can be generated from this class as :class:`SupportiveSkillEntry`. Each entry contains exactly one buff.
    """

    action_condition_asset: InitVar[ActionConditionAsset]

    buffs_base: list[set[ActionConditionEffectUnit]] = field(init=False)
    """
    Base buffs. These buffs will be granted without any additional conditions.

    Calling ``buffs_base[skill_lv]`` will return a set of buffs at ``skill_lv``.
    """
    buffs_teammate_coverage: list[list[set[ActionConditionEffectUnit]]] = field(init=False)
    """
    Buffs to be granted for different count of teammates covered.

    Calling ``buffs_teammate_coverage[skill_lv][teammate_count]`` will return a set of buffs at ``skill_lv``
    when ``teammate_count`` covered.
    """
    buffs_elemental: list[dict[Element, set[ActionConditionEffectUnit]]] = field(init=False)
    """
    Buffs to be granted only if the target element matches.

    Calling ``buffs_elemental[skill_lv][element_enum]`` will return a set of buffs at ``skill_lv``
    when the target element is ``element_enum``.
    """
    buffs_pre_conditioned: list[dict[SkillCondition, set[ActionConditionEffectUnit]]] = field(init=False)
    """
    Buffs to be granted only if the condition matches.

    Calling ``buffs_hp_condition[skill_lv][skill_condition]`` will return a set of buffs at ``skill_lv``
    when the target condition matches ``skill_condition``.
    """

    def _init_all_possible_conditions(self, action_condition_asset: ActionConditionAsset):
        # Check availabilities
        has_teammate_coverage: bool = any(
            hit_data.hit_attr.has_hit_condition
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        # noinspection PyUnboundLocalVariable
        has_elemental_restriction: bool = any(
            entry.target_limited_by_element
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
            if (hit_data.hit_attr.has_action_condition
                and (entry := action_condition_asset.get_data_by_id(hit_data.hit_attr.action_condition_id)))
        )

        # Initialization
        cond_elems: list[set[tuple[SkillCondition, ...]]] = self._init_possible_conditions_base_elems()

        # Teammate coverage conditions available
        if has_teammate_coverage:
            cond_elems.append({(teammate_coverage_cond,) for teammate_coverage_cond
                               in SkillConditionCategories.skill_teammates_covered.members})

        # Elemental restriction available
        if has_elemental_restriction:
            cond_elems.append({(target_element_cond,)
                               for target_element_cond in SkillConditionCategories.target_element.members
                               if any(buffs_lv[SkillConditionCategories.target_element.convert(target_element_cond)]
                                      for buffs_lv in self.buffs_elemental)})

        # Add combinations
        self.possible_conditions = {
            SkillConditionComposite(tuple(subitem for item in item_combination for subitem in item))
            for item_combination in product(*cond_elems)
        }

    def _init_base_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_base = []

        for hit_data_lv in self.hit_data_mtx:
            buff_lv = set()

            for hit_data in hit_data_lv:
                if hit_data.hit_attr.has_hit_condition:
                    # Skip conditions that require teammate coverage, let ``buffs_teammate_coverage`` handles this
                    continue

                if hit_data.hit_attr.has_action_condition:
                    action_condition = action_condition_asset.get_data_by_id(hit_data.hit_attr.action_condition_id)
                    if action_condition.target_limited_by_element:
                        # Skip conditions that require certain elements, let ``buffs_elemental`` handles this
                        continue

                if hit_data.pre_condition:
                    # Skip conditions that has pre condition, let ``buffs_pre_conditioned`` handles this
                    continue

                buff_lv.update(hit_data.to_buffing_units(action_condition_asset))

            self.buffs_base.append(buff_lv)

    def _init_teammate_coverage_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_teammate_coverage: list[list[set[ActionConditionEffectUnit]]] = []

        teammate_coverage_counts = SkillConditionCategories.skill_teammates_covered.targets

        for hit_data_lv in self.hit_data_mtx:
            buff_lv: list[set[ActionConditionEffectUnit]] = [set() for _ in teammate_coverage_counts]

            for hit_data in hit_data_lv:
                hit_attr = hit_data.hit_attr

                for teammate_count in teammate_coverage_counts:
                    if not hit_attr.has_hit_condition:
                        continue  # No skill hit condition

                    # Currently, only Nadine S1, S!Cleo S2 and Laranoa S2 uses teammate coverage condition.
                    # This calculation allows us to get the offset of the conditions,
                    # then subtract the offset with the boundaries to get the teammates coverage count.
                    hit_cond_offset = min(hit_attr.hit_condition_lower_bound, hit_attr.hit_condition_upper_bound) + 1
                    if teammate_count < hit_attr.hit_condition_lower_bound - hit_cond_offset:
                        continue  # Teammate # lower than the boundary
                    if (
                            hit_attr.hit_condition_upper_bound  # This will be 0 if no upper limit
                            and teammate_count > hit_attr.hit_condition_upper_bound - hit_cond_offset
                    ):
                        continue  # Teammate # higher than the boundary

                    buff_lv[teammate_count].update(hit_data.to_buffing_units(action_condition_asset))

            self.buffs_teammate_coverage.append(buff_lv)

    def _init_elemental_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_elemental: list[dict[Element, set[ActionConditionEffectUnit]]] = []

        for hit_data_lv in self.hit_data_mtx:
            buff_lv: dict[Element, set[ActionConditionEffectUnit]] = {
                elem: set() for elem in Element.get_all_valid_elements()
            }

            for hit_data in hit_data_lv:
                if not hit_data.hit_attr.has_action_condition:
                    continue  # No action condition assigned

                action_condition = action_condition_asset.get_data_by_id(hit_data.hit_attr.action_condition_id)

                if not action_condition.target_limited_by_element:
                    continue  # Action condition not limited by element

                for elem in Element.get_all_valid_elements():
                    if elem.to_flag() not in action_condition.elemental_target:
                        continue

                    buff_lv[elem].update(hit_data.to_buffing_units(action_condition_asset))

            self.buffs_elemental.append(buff_lv)

    def _init_pre_conditioned_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_pre_conditioned: list[dict[SkillCondition, set[ActionConditionEffectUnit]]] = []

        for hit_data_lv in self.hit_data_mtx:
            buff_lv: dict[SkillCondition, set[ActionConditionEffectUnit]] = defaultdict(set)

            for hit_data in hit_data_lv:
                buff_lv[hit_data.pre_condition].update(hit_data.to_buffing_units(action_condition_asset))

            self.buffs_pre_conditioned.append(dict(buff_lv))

    def __post_init__(self, action_condition_asset: ActionConditionAsset):
        self._init_base_buffs(action_condition_asset)
        self._init_teammate_coverage_buffs(action_condition_asset)
        self._init_elemental_buffs(action_condition_asset)
        self._init_pre_conditioned_buffs(action_condition_asset)

        super().__post_init__(action_condition_asset)

    def with_conditions(self, condition_comp: Optional[SkillConditionComposite] = None) -> SupportiveSkillEntry:
        if not condition_comp:
            condition_comp = SkillConditionComposite()  # Dummy empty condition composite

        # Deep copy buff base
        buffs: list[set[ActionConditionEffectUnit]] = [buff_set.copy() for buff_set in self.buffs_base]

        # Attach teammate coverage only buffs
        if condition_comp.teammate_coverage:
            for skill_lv in range(self.max_level):
                buffs[skill_lv].update(
                    self.buffs_teammate_coverage[skill_lv][condition_comp.teammate_coverage_converted]
                )

        # Attach elemental buffs
        if condition_comp.target_element:
            for skill_lv in range(self.max_level):
                buffs[skill_lv].update(self.buffs_elemental[skill_lv][condition_comp.target_element_converted])

        # Attach pre-conditioned buffs, if matches
        for skill_lv in range(self.max_level):
            for condition in condition_comp:
                # Conditions in ``condition_comp`` could be non-pre-condition
                buffs[skill_lv].update(self.buffs_pre_conditioned[skill_lv].get(condition, set()))

        return SupportiveSkillEntry(condition_comp=condition_comp, buffs=buffs)

    @property
    def max_level(self) -> int:
        """
        Get the max level of the skill.

        This is **NOT** the actual in-game max level.
        """
        return len(self.hit_data_mtx)
