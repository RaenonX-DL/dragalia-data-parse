"""Class for a single supportive skill entry."""
from dataclasses import dataclass, field, InitVar
from itertools import product
from typing import Optional

from dlparse.enums import (
    SkillConditionComposite, SkillCondition, SkillConditionCategories,
    HitTargetSimple, BuffParameter, SkillIndex, Element
)
from dlparse.mono.asset import ActionConditionAsset, ActionConditionEntry, HitAttrEntry
from .hit_buff import BuffingHitData
from .skill_base import SkillDataBase, SkillEntryBase

__all__ = ("SupportiveSkillUnit", "SupportiveSkillEntry", "SupportiveSkillData")


@dataclass
class SupportiveSkillUnit:
    """The atomic unit of an effect of a supportive skill at a certain level."""

    target: HitTargetSimple
    parameter: BuffParameter
    rate: float
    duration_time: float
    duration_count: float

    hit_attr_label: str
    action_cond_id: int

    def __hash__(self):
        return hash((self.target, self.parameter, self.rate, self.duration_time, self.duration_count,
                     self.hit_attr_label, self.action_cond_id))

    def __eq__(self, other):
        if not isinstance(other, SupportiveSkillUnit):
            return False

        return hash(self) == hash(other)


@dataclass
class SupportiveSkillEntry(SkillEntryBase):
    """
    A single entry for a supportive skill. This contains all buffs across all levels under a certain condition.

    To get the buffs at a certain level, use ``self.buffs[skill_lv - 1]``.
    """

    buffs: list[set[SupportiveSkillUnit]]


class SupportiveSkillConverter:
    """Class for converting a supportive skill to a single buff entry."""

    @staticmethod
    def to_param_up(param_enum: BuffParameter, param_rate: float,
                    hit_attr: HitAttrEntry, cond_entry: Optional[ActionConditionEntry]) \
            -> Optional[SupportiveSkillUnit]:
        """
        Create a buff unit (if applicable) based on the given data.

        If ``param_rate`` is ``0`` (meaning not used), ``None`` will be returned instead.

        if ``cond_entry`` is ``None``, both ``duration_time`` and ``duration_count`` will set to 0.
        """
        if not param_rate:  # Param rate = 0 means not applicable
            return None

        return SupportiveSkillUnit(
            target=hit_attr.target_group.to_simple(),
            parameter=param_enum,
            rate=param_rate,
            duration_time=cond_entry.duration_sec if cond_entry else 0,
            duration_count=cond_entry.duration_count if cond_entry else 0,
            hit_attr_label=hit_attr.id,
            action_cond_id=hit_attr.action_condition_id
        )

    @staticmethod
    def convert_to_units(hit_attr: HitAttrEntry, action_condition_asset: ActionConditionAsset) \
            -> set[SupportiveSkillUnit]:
        """Convert ``hit_attr`` to a set of :class:`SupportiveSkillUnit`."""
        entries: set[Optional[SupportiveSkillUnit]] = set()

        # Get the action condition entry
        cond_entry: ActionConditionEntry = action_condition_asset.get_data_by_id(hit_attr.action_condition_id)

        # --- General buffs

        if cond_entry:
            # ATK buff
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.ATK, cond_entry.buff_atk, hit_attr, cond_entry))
            # DEF buff
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.DEF, cond_entry.buff_def, hit_attr, cond_entry))
            # CRT rate
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.CRT_RATE, cond_entry.buff_crt_rate, hit_attr, cond_entry))
            # CRT damage
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.CRT_DAMAGE, cond_entry.buff_crt_damage, hit_attr, cond_entry))
            # Skill damage
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.SKILL_DAMAGE, cond_entry.buff_skill_damage, hit_attr, cond_entry))
            # SP rate
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.SP_RATE, cond_entry.buff_sp_rate, hit_attr, cond_entry))

        # --- Instant gauge refill

        # SP charge %
        if skill_idx := SkillIndex(hit_attr.sp_recov_skill_idx_2):  # idx 2 always give more accurate result
            if skill_idx == SkillIndex.S1:
                entries.add(SupportiveSkillConverter.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_S1, hit_attr.sp_recov_ratio, hit_attr, cond_entry))
            if skill_idx == SkillIndex.S2:
                entries.add(SupportiveSkillConverter.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_S2, hit_attr.sp_recov_ratio, hit_attr, cond_entry))

        # Pop off the ``None`` element (``None`` will be added on entry ineffective)
        entries.discard(None)

        return entries


@dataclass
class SupportiveSkillData(SkillDataBase[BuffingHitData, SupportiveSkillEntry]):
    """
    A supportive skill data.

    All buffs can be generated from this class as :class:`SupportiveSkillEntry`. Each entry contains exactly one buff.
    """

    action_condition_asset: InitVar[ActionConditionAsset]

    buffs_base: list[set[SupportiveSkillUnit]] = field(init=False)
    """
    Base buffs. These buffs will be granted without any additional conditions.

    Calling ``buffs_base[skill_lv]`` will return a set of buffs at ``skill_lv``.
    """
    buffs_teammate_coverage: list[list[set[SupportiveSkillUnit]]] = field(init=False)
    """
    Buffs to be granted for different count of teammates covered.

    Calling ``buffs_teammate_coverage[skill_lv][teammate_count]`` will return a set of buffs at ``skill_lv``
    when ``teammate_count`` covered.
    """
    buffs_elemental: list[dict[Element, set[SupportiveSkillUnit]]] = field(init=False)
    """
    Buffs to be granted ont if the target element matches.

    Calling ``buffs_elemental[skill_lv][element_enum]`` will return a set of buffs at ``skill_lv``
    when the target element is ``element_enum``.
    """

    def _init_all_possible_conditions(self):
        has_teammate_coverage: bool = False

        # Check availabilities
        for hit_data_lv in self.hit_data_mtx:
            for hit_data in hit_data_lv:
                has_teammate_coverage = has_teammate_coverage or hit_data.hit_attr.has_hit_condition

        cond_elems: list[set[tuple[SkillCondition, ...]]] = []

        # Teammate coverage conditions available, attach it
        if has_teammate_coverage:
            cond_elems.append({(teammate_coverage_cond,) for teammate_coverage_cond
                               in SkillConditionCategories.skill_teammates_covered.members})

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
                hit_attr = hit_data.hit_attr

                if hit_attr.has_hit_condition:
                    # Skip conditions that require teammate coverage, let ``buffs_teammate_coverage`` handles this
                    continue

                if hit_attr.has_action_condition:
                    action_condition = action_condition_asset.get_data_by_id(hit_attr.action_condition_id)
                    if action_condition.target_limited_by_element:
                        # Skip conditions that require certain elements, let ``buffs_elemental`` handles this
                        continue

                if skill_entries := SupportiveSkillConverter.convert_to_units(hit_attr, action_condition_asset):
                    buff_lv |= skill_entries

            self.buffs_base.append(buff_lv)

    def _init_teammate_coverage_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_teammate_coverage: list[list[set[SupportiveSkillUnit]]] = []

        teammate_coverage_counts = SkillConditionCategories.skill_teammates_covered.targets

        for hit_data_lv in self.hit_data_mtx:
            buff_lv: list[set[SupportiveSkillUnit]] = [set() for _ in teammate_coverage_counts]

            for hit_data in hit_data_lv:
                hit_attr = hit_data.hit_attr

                for teammate_count in teammate_coverage_counts:
                    if not hit_attr.has_hit_condition:
                        continue  # No skill hit condition

                    # Currently, only Nadine S1, S!Cleo S2 and Laranoa S2 uses teammate coverage condition.
                    # This calculation allows us to get the offset of the conditions,
                    # then subtract the offset with the boundaries to get the teammates coverage count.
                    hit_cond_offset = min(hit_attr.hit_condition_lower_bound, hit_attr.hit_condition_upper_bound)
                    if teammate_count < hit_attr.hit_condition_lower_bound - hit_cond_offset:
                        continue  # Teammate # lower than the boundary
                    if (
                            hit_attr.hit_condition_upper_bound  # This will be 0 if no upper limit
                            and teammate_count > hit_attr.hit_condition_upper_bound - hit_cond_offset
                    ):
                        continue  # Teammate # higher than the boundary

                    if skill_entries := SupportiveSkillConverter.convert_to_units(hit_attr, action_condition_asset):
                        buff_lv[teammate_count] |= skill_entries

            self.buffs_teammate_coverage.append(buff_lv)

    def _init_elemental_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_elemental: list[dict[Element, set[SupportiveSkillUnit]]] = []

        for hit_data_lv in self.hit_data_mtx:
            buff_lv: dict[Element, set[SupportiveSkillUnit]] = {elem: set()
                                                                for elem in Element.get_all_valid_elements()}

            for hit_data in hit_data_lv:
                hit_attr = hit_data.hit_attr

                if not hit_attr.has_action_condition:
                    continue  # No action condition assigned

                action_condition = action_condition_asset.get_data_by_id(hit_attr.action_condition_id)

                if not action_condition.target_limited_by_element:
                    continue  # Action condition not limited by element

                for elem in Element.get_all_valid_elements():
                    if elem.to_flag() in action_condition.elemental_target:
                        buff_lv[elem] |= SupportiveSkillConverter.convert_to_units(hit_attr, action_condition_asset)

            self.buffs_elemental.append(buff_lv)

    def __post_init__(self, action_condition_asset: ActionConditionAsset):  # pylint: disable=arguments-differ
        super().__post_init__()

        self._init_base_buffs(action_condition_asset)
        self._init_teammate_coverage_buffs(action_condition_asset)
        self._init_elemental_buffs(action_condition_asset)

    def with_conditions(self, condition_comp: SkillConditionComposite = None) -> SupportiveSkillEntry:
        if not condition_comp:
            condition_comp = SkillConditionComposite()  # Dummy empty condition composite

        # Deep copy buff base
        buffs: list[set[SupportiveSkillUnit]] = [buff_set.copy() for buff_set in self.buffs_base]

        # Attach teammate coverage only buffs
        if condition_comp.teammate_coverage:
            for skill_lv in range(self.max_level):
                buffs[skill_lv] |= self.buffs_teammate_coverage[skill_lv][condition_comp.teammate_coverage_converted]

        # Attach elemental buffs
        if condition_comp.target_elemental:
            for skill_lv in range(self.max_level):
                buffs[skill_lv] |= self.buffs_elemental[skill_lv][condition_comp.target_elemental_converted]

        return SupportiveSkillEntry(condition_comp=condition_comp, buffs=buffs)

    @property
    def max_level(self) -> int:
        """
        Get the max level of the skill.

        This is **NOT** the actual in-game max level.
        """
        return len(self.hit_data_mtx)