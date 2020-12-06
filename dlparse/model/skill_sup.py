"""Class for a single supportive skill entry."""
from collections import defaultdict
from dataclasses import InitVar, dataclass, field
from itertools import product
from typing import Optional

from dlparse.enums import (
    BuffParameter, Element, HitTargetSimple, SkillCondition, SkillConditionCategories, SkillConditionComposite,
    SkillIndex,
)
from dlparse.errors import UnhandledSelfDamageError
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

    max_stack_count: int
    """
    Maximum count of the buffs stackable.

    ``0`` means not applicable (``duration_count`` = 0, most likely is a buff limited by time duration).

    ``1`` means unstackable.

    Any positive number means the maximum count of stacks possible.
    """

    def __hash__(self):
        return hash((self.hit_attr_label, self.action_cond_id))

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

    @property
    def max_lv_buffs(self) -> set[SupportiveSkillUnit]:
        """Get the buffs at the max level."""
        return self.buffs[-1]


class SupportiveSkillConverter:
    """Class for converting a supportive skill to a single buff entry."""

    @staticmethod
    def to_param_up(
            param_enum: BuffParameter, param_rate: float,
            hit_data: BuffingHitData, cond_entry: Optional[ActionConditionEntry]
    ) -> Optional[SupportiveSkillUnit]:
        """
        Create a buff unit (if applicable) based on the given data.

        If ``param_rate`` is ``0`` (meaning not used), ``None`` will be returned instead.

        if ``cond_entry`` is ``None``, both ``duration_time`` and ``duration_count`` will set to 0.
        """
        if not param_rate:  # Param rate = 0 means not applicable
            return None

        return SupportiveSkillUnit(
            target=hit_data.target_simple,
            parameter=param_enum,
            rate=param_rate,
            duration_time=hit_data.get_duration(cond_entry),
            duration_count=cond_entry.duration_count if cond_entry else 0,
            hit_attr_label=hit_data.hit_attr.id,
            action_cond_id=hit_data.hit_attr.action_condition_id,
            max_stack_count=cond_entry.duration_count_max if cond_entry else 0
        )

    @staticmethod
    def to_damage_self(hit_attr: HitAttrEntry) -> Optional[SupportiveSkillUnit]:
        """
        Returns the corresponding :class:`SupportiveSkillUnit` if the hit attribute will self damage.

        Returns ``None`` if not self damaging.

        :raises UnhandledSelfDamageError: if the self damage ability is unhandled
        """
        if not hit_attr.is_damage_self:
            return None

        if hit_attr.hp_fix_rate:
            return SupportiveSkillUnit(
                target=HitTargetSimple.SELF,
                parameter=BuffParameter.HP_FIX_BY_MAX,
                rate=hit_attr.hp_fix_rate,
                duration_time=0,
                duration_count=0,
                hit_attr_label=hit_attr.id,
                action_cond_id=hit_attr.action_condition_id,
                max_stack_count=0
            )

        if hit_attr.hp_consumption_rate:
            return SupportiveSkillUnit(
                target=HitTargetSimple.SELF,
                parameter=BuffParameter.HP_DECREASE_BY_MAX,
                rate=hit_attr.hp_consumption_rate,
                duration_time=0,
                duration_count=0,
                hit_attr_label=hit_attr.id,
                action_cond_id=hit_attr.action_condition_id,
                max_stack_count=0
            )

        raise UnhandledSelfDamageError(hit_attr.id)

    @staticmethod
    def convert_to_units(
            hit_data: BuffingHitData, action_condition_asset: ActionConditionAsset
    ) -> set[SupportiveSkillUnit]:
        """Convert ``hit_data`` to a set of :class:`SupportiveSkillUnit`."""
        entries: set[Optional[SupportiveSkillUnit]] = set()

        # Get the action condition entry
        cond_entry: ActionConditionEntry = action_condition_asset.get_data_by_id(hit_data.hit_attr.action_condition_id)

        # --- Conditions in action condition

        entries.add(SupportiveSkillConverter.to_damage_self(hit_data.hit_attr))

        # --- General buffs

        if cond_entry:
            # ATK
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.ATK, cond_entry.buff_atk, hit_data, cond_entry))
            # DEF
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.DEF, cond_entry.buff_def, hit_data, cond_entry))
            # CRT rate
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.CRT_RATE, cond_entry.buff_crt_rate, hit_data, cond_entry))
            # CRT damage
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.CRT_DAMAGE, cond_entry.buff_crt_damage, hit_data, cond_entry))
            # Skill damage
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.SKILL_DAMAGE, cond_entry.buff_skill_damage, hit_data, cond_entry))
            # FS damage
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.FS_DAMAGE, cond_entry.buff_fs_damage, hit_data, cond_entry))
            # ATK SPD
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.ATK_SPD, cond_entry.buff_atk_spd, hit_data, cond_entry))
            # FS SPD
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.FS_SPD, cond_entry.buff_fs_spd, hit_data, cond_entry))
            # SP rate
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.SP_RATE, cond_entry.buff_sp_rate, hit_data, cond_entry))

            # Damage Shield
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.SHIELD_SINGLE_DMG, cond_entry.shield_dmg, hit_data, cond_entry))
            # HP Shield
            entries.add(SupportiveSkillConverter.to_param_up(
                BuffParameter.SHIELD_LIFE, cond_entry.shield_hp, hit_data, cond_entry))

        # --- Instant gauge refill

        # SP charge %
        # idx 2 always give more accurate result (at least S!Cleo is giving the correct one)
        if skill_idx := SkillIndex(hit_data.hit_attr.sp_recov_skill_idx_2):
            if skill_idx == SkillIndex.S1:
                entries.add(SupportiveSkillConverter.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_S1, hit_data.hit_attr.sp_recov_ratio, hit_data, cond_entry))
            elif skill_idx == SkillIndex.S2:
                entries.add(SupportiveSkillConverter.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_S2, hit_data.hit_attr.sp_recov_ratio, hit_data, cond_entry))
            elif skill_idx == SkillIndex.USED_SKILL:
                entries.add(SupportiveSkillConverter.to_param_up(
                    BuffParameter.SP_CHARGE_PCT_USED, hit_data.hit_attr.sp_recov_ratio, hit_data, cond_entry))

        # Pop off the ``None`` element (``None`` will be added if the entry is ineffective)
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
    Buffs to be granted only if the target element matches.

    Calling ``buffs_elemental[skill_lv][element_enum]`` will return a set of buffs at ``skill_lv``
    when the target element is ``element_enum``.
    """
    buffs_pre_conditioned: list[dict[SkillCondition, set[SupportiveSkillUnit]]] = field(init=False)
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
                               for target_element_cond in SkillConditionCategories.target_elemental.members
                               if any(buffs_lv[SkillConditionCategories.target_elemental.convert(target_element_cond)]
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

                if skill_entries := SupportiveSkillConverter.convert_to_units(hit_data, action_condition_asset):
                    buff_lv.update(skill_entries)

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
                    hit_cond_offset = min(hit_attr.hit_condition_lower_bound, hit_attr.hit_condition_upper_bound) + 1
                    if teammate_count < hit_attr.hit_condition_lower_bound - hit_cond_offset:
                        continue  # Teammate # lower than the boundary
                    if (
                            hit_attr.hit_condition_upper_bound  # This will be 0 if no upper limit
                            and teammate_count > hit_attr.hit_condition_upper_bound - hit_cond_offset
                    ):
                        continue  # Teammate # higher than the boundary

                    if skill_entries := SupportiveSkillConverter.convert_to_units(hit_data, action_condition_asset):
                        buff_lv[teammate_count].update(skill_entries)

            self.buffs_teammate_coverage.append(buff_lv)

    def _init_elemental_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_elemental: list[dict[Element, set[SupportiveSkillUnit]]] = []

        for hit_data_lv in self.hit_data_mtx:
            buff_lv: dict[Element, set[SupportiveSkillUnit]] = {elem: set()
                                                                for elem in Element.get_all_valid_elements()}

            for hit_data in hit_data_lv:
                if not hit_data.hit_attr.has_action_condition:
                    continue  # No action condition assigned

                action_condition = action_condition_asset.get_data_by_id(hit_data.hit_attr.action_condition_id)

                if not action_condition.target_limited_by_element:
                    continue  # Action condition not limited by element

                for elem in Element.get_all_valid_elements():
                    if elem.to_flag() in action_condition.elemental_target:
                        buff_lv[elem].update(
                            SupportiveSkillConverter.convert_to_units(hit_data, action_condition_asset)
                        )

            self.buffs_elemental.append(buff_lv)

    def _init_pre_conditioned_buffs(self, action_condition_asset: ActionConditionAsset):
        self.buffs_pre_conditioned: list[dict[SkillCondition, set[SupportiveSkillUnit]]] = []

        for hit_data_lv in self.hit_data_mtx:
            buff_lv: dict[SkillCondition, set[SupportiveSkillUnit]] = defaultdict(set)

            for hit_data in hit_data_lv:
                sup_skill_unit = SupportiveSkillConverter.convert_to_units(hit_data, action_condition_asset)
                buff_lv[hit_data.pre_condition].update(sup_skill_unit)

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
        buffs: list[set[SupportiveSkillUnit]] = [buff_set.copy() for buff_set in self.buffs_base]

        # Attach teammate coverage only buffs
        if condition_comp.teammate_coverage:
            for skill_lv in range(self.max_level):
                buffs[skill_lv].update(
                    self.buffs_teammate_coverage[skill_lv][condition_comp.teammate_coverage_converted]
                )

        # Attach elemental buffs
        if condition_comp.target_elemental:
            for skill_lv in range(self.max_level):
                buffs[skill_lv].update(self.buffs_elemental[skill_lv][condition_comp.target_elemental_converted])

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
