"""Models for character skills."""
from dataclasses import InitVar, dataclass, field
from itertools import combinations, product, zip_longest
from typing import Optional

from dlparse.enums import Condition, ConditionCategories, ConditionComposite, HitTargetSimple, Status
from dlparse.mono.asset import ActionConditionAsset, BuffCountAsset
from .action_cond_effect import HitActionConditionEffectUnit
from .base import SkillDataBase, SkillEntryBase
from .buff_boost import BuffCountBoostData, BuffFieldBoostData
from .hit_dmg import DamageUnit, DamagingHitData
from .unit_cancel import SkillCancelActionUnit
from .unit_mod import DamageModifierUnit

__all__ = ("AttackingSkillDataEntry", "AttackingSkillData")


@dataclass
class AttackingSkillDataEntry(SkillEntryBase):
    """
    An entry of the attacking skill data.

    Both ``hit_count`` and ``mods`` should be sorted by the skill level.

    For example, if skill level 1 has 1 hit and 100% mods while skill level 2 has 2 hits and 150% + 200% mods,
    ``hit_count`` should be ``[1, 2]`` and ``mods`` should be ``[[1.0], [1.5, 2.0]]``.

    The relationship between the ``conditions`` are **AND**, which means that all conditions must be true.

    .. note::
        Hit count could be 0, since a skill may be attacking and supportive combined across the levels
        (OG Elisanne S1 - `105402011`).
    """

    asset_action_cond: InitVar[ActionConditionAsset]  # Used for effect unit categorizing
    asset_buff_count: InitVar[BuffCountAsset]  # Used for buff boost data extracting

    hit_unit_mtx: list[list[DamageUnit]]
    hit_count: list[int]

    cancel_unit_mtx: list[list[SkillCancelActionUnit]]

    buff_field_boost_mtx: list[BuffFieldBoostData]

    mod_unit_mtx: list[list[DamageModifierUnit]] = field(init=False)

    afflictions: list[list[HitActionConditionEffectUnit]] = field(init=False)
    debuffs: list[list[HitActionConditionEffectUnit]] = field(init=False)

    dispel_timings: list[list[float]] = field(init=False)

    def _init_debuff(self, asset_action_cond: ActionConditionAsset):
        self.debuffs = []
        for hit_unit_lv in self.hit_unit_mtx:
            debuff_units_lv = []

            for hit_unit in hit_unit_lv:
                if not hit_unit.unit_debuffs:
                    continue  # No debuff units available, skip it

                if not hit_unit.hit_attr.action_condition_id:
                    # No action condition bound to the hit attribute, add all debuff units directly
                    debuff_units_lv.extend(hit_unit.unit_debuffs)
                    continue

                # Action condition bound to the hit unit, check that
                action_cond = asset_action_cond.get_data_by_id(hit_unit.hit_attr.action_condition_id)
                action_cond_conditions = action_cond.conditions

                if (
                        action_cond_conditions
                        and not any(elem_cond in self.condition_comp for elem_cond in action_cond_conditions)
                ):
                    # No condition of the action condition matches,
                    # debuff units of the action condition should not work
                    continue

                debuff_units_lv.extend(hit_unit.unit_debuffs)

            self.debuffs.append(debuff_units_lv)

    def _init_mod_unit_mtx(self, asset_action_cond: ActionConditionAsset, asset_buff_count: BuffCountAsset):
        self.mod_unit_mtx = []
        for hit_unit_lv in self.hit_unit_mtx:
            mod_unit_lv = []

            for hit_unit in hit_unit_lv:
                buff_boost_data = BuffCountBoostData.from_hit_attr(
                    hit_unit.hit_attr, self.condition_comp, asset_action_cond, asset_buff_count
                )

                mod_unit_lv.append(DamageModifierUnit(
                    hit_unit.mod, hit_unit.hit_attr.rate_boost_on_crisis, hit_unit.counter_mod, buff_boost_data
                ))

            self.mod_unit_mtx.append(mod_unit_lv)

    def _init_dispel_buff_timings(self, asset_action_cond: ActionConditionAsset):
        self.dispel_timings = []
        for hit_unit_lv in self.hit_unit_mtx:
            dispel_timing_lv = []

            for hit_unit in hit_unit_lv:
                if not hit_unit.hit_attr.has_action_condition:
                    continue

                action_cond = asset_action_cond.get_data_by_id(hit_unit.hit_attr.action_condition_id)

                if action_cond.is_dispel_buff:
                    dispel_timing_lv.append(hit_unit.hit_time)

            self.dispel_timings.append(dispel_timing_lv)

    def __post_init__(self, asset_action_cond: ActionConditionAsset, asset_buff_count: BuffCountAsset):
        self._init_mod_unit_mtx(asset_action_cond, asset_buff_count)

        self._init_dispel_buff_timings(asset_action_cond)

        self.afflictions = [
            [hit_unit.unit_affliction for hit_unit in hit_unit_lv if hit_unit.unit_affliction]
            for hit_unit_lv in self.hit_unit_mtx
        ]
        self._init_debuff(asset_action_cond)

    @property
    def mods(self) -> list[list[float]]:
        """
        Get the original damage modifier distribution at each level.

        The 1st dimension is the skill level, and the 2nd dimension is each hit.

        Mods = ``0`` will not be returned.
        """
        return [
            [mod_unit.original for mod_unit in mod_unit_lv if mod_unit.original]
            for mod_unit_lv in self.mod_unit_mtx
        ]

    @property
    def hit_timings(self) -> list[list[float]]:
        """
        Get the hit connecting timings at each level.

        The 1st dimension is the skill level, and the 2nd dimension is each hit.

        Mods = ``0`` will not be returned.
        """
        return [
            [hit_unit.hit_time for hit_unit in hit_unit_lv if hit_unit.mod]
            for hit_unit_lv in self.hit_unit_mtx
        ]

    @property
    def total_mod(self) -> list[float]:
        """Get the total original damage modifiers at each level."""
        return [sum(mods) for mods in self.mods]

    @property
    def counter_mods(self) -> list[list[float]]:
        """
        Get the counter damage modifier distribution at each level.

        The 1st dimension is the skill level, and the 2nd dimension is each hit.

        Every hit will be returned, even if it does not have counter damage modifier.
        """
        return [
            [mod_unit.counter for mod_unit in mod_unit_lv]
            for mod_unit_lv in self.mod_unit_mtx
        ]

    @property
    def crisis_mods(self) -> list[list[float]]:
        """
        Get the crsis damage modifier distribution at each level.

        The 1st dimension is the skill level, and the 2nd dimension is each hit.

        Every hit will be returned, even if it does not have crsis damage modifier.
        """
        return [
            [mod_unit.crisis for mod_unit in mod_unit_lv]
            for mod_unit_lv in self.mod_unit_mtx
        ]

    @property
    def total_counter_mod(self) -> list[float]:
        """Get the total counter damage modifiers at each level."""
        return [sum(counter_mod) for counter_mod in self.counter_mods]

    @property
    def buff_count_boost_mtx(self) -> list[list[BuffCountBoostData]]:
        """
        Get the buff count boost data at each level.

        The 1st dimension is the skill level, and the 2nd dimension is each hit.
        """
        return [
            [mod_unit.buff_boost_data for mod_unit in mod_unit_lv if mod_unit.buff_boost_data]
            for mod_unit_lv in self.mod_unit_mtx
        ]

    @property
    def hit_count_at_max(self) -> int:
        """Get the skill hit count at the max level."""
        return self.hit_count[self.max_level - 1]

    @property
    def total_mod_at_max(self) -> float:
        """Get the total skill modifier at the max level."""
        return self.total_mod[self.max_level - 1]

    @property
    def mods_at_max(self) -> list[float]:
        """Get the skill modifiers at the max level."""
        return self.mods[self.max_level - 1]

    @property
    def total_counter_mod_at_max(self) -> float:
        """Get the total counter damage modifier at the max level."""
        return self.total_counter_mod[self.max_level - 1]

    @property
    def counter_mod_at_max(self) -> list[float]:
        """Get the counter damage modifiers at the max level."""
        return self.counter_mods[self.max_level - 1]

    @property
    def has_effects_on_enemy(self) -> bool:
        """Check if there are any effects which target is the enemy."""
        if any(any(mod.original for mod in mod_unit_lv) for mod_unit_lv in self.mod_unit_mtx):
            # Has mod > 0
            return True

        if any(
                any(affliction.target == HitTargetSimple.ENEMY for affliction in affliction_lv)
                for affliction_lv in self.afflictions
        ):
            # Afflicts enemy
            return True

        if any(
                any(debuff.target == HitTargetSimple.ENEMY for debuff in debuff_lv)
                for debuff_lv in self.debuffs
        ):
            # Debuffs enemy
            return True

        return False

    @property
    def dispel_buff(self) -> list[bool]:
        """Check if dispel is available at each level."""
        # Dispel timing could be 0.0, therefore calling any() doesn't work because it gives false negative
        return [len(dispel_timings) > 0 for dispel_timings in self.dispel_timings]

    @property
    def dispel_buff_at_max(self) -> bool:
        """Check if dispel is available at the maximum level."""
        return self.dispel_buff[-1]


@dataclass
class AttackingSkillData(SkillDataBase[DamagingHitData, AttackingSkillDataEntry]):
    """
    An attacking skill data.

    Skill data under different condition can be generated from this class as :class:`AttackingSkillDataEntry`.

    .. note::
        The implementation of ``max_level`` is to get the level which has the highest mods.
        If 2 levels sharing the same total damage, the higher level will be considered as "max" level.

        The reason of such implmentation is due to the fact that
        the game may have inserted some dummy data for a higher level.

        For example, OG!Zena S2 has label with "LV03" detected. However, she does not have Lv.3 S2 yet
        (as of 2020/11/24). Containing the info of Lv.3 usually gives wrong result
        because the implementation is incomplete.

        Note that this still does **NOT** reflect the actual in-game max level.
        The data of Templar Hope S2 at Lv.3 has been already inserted (and it's the highest damage output level).
        However, he does not have 70 MC yet.

        To get the actual max skill level in-game, character data is needed.
    """

    # Indicate if the sectioned conditions should be included in possible conditions
    is_exporting: InitVar[bool]

    cancel_unit_mtx_base: list[list[SkillCancelActionUnit]] = field(init=False)

    _unit_mtx_base: list[list[DamageUnit]] = field(init=False)
    _buff_field_boost_mtx: list[BuffFieldBoostData] = field(init=False)

    _has_non_zero_mods: bool = field(init=False)

    def _init_all_possible_conditions_target(self):
        cond_elems: list[set[tuple[Condition, ...]]] = []

        # OD / BK boosts available
        od_boost_available: bool = any(
            hit_data.hit_attr.boost_in_od for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        if od_boost_available:
            cond_elems.append({(Condition.TARGET_OD_STATE,)})
        bk_boost_available: bool = any(
            hit_data.hit_attr.boost_in_bk for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        if bk_boost_available:
            cond_elems.append({(Condition.TARGET_BK_STATE,)})

        # Punishers available
        punishers_available: set[Status] = {
            punisher_state
            for hit_data_lv in self.hit_data_mtx
            for hit_data in hit_data_lv
            for punisher_state in hit_data.hit_attr.punisher_states
        }
        if punishers_available:
            conditions: set[Condition] = {
                ConditionCategories.target_status.convert_reversed(affliction)
                for affliction in punishers_available
            }
            # noinspection PyTypeChecker
            affliction_combinations: set[tuple[Condition, ...]] = set()
            for count in range(len(conditions) + 1):
                affliction_combinations.update(combinations(conditions, count))

            cond_elems.append(affliction_combinations)

        return cond_elems

    def _init_all_possible_conditions_self_crisis_buff(self, is_exporting: bool):
        cond_elems: list[set[tuple[Condition, ...]]] = []

        # Crisis boosts available (skip adding sectioned HP if exporting)
        if not is_exporting:
            crisis_available: bool = any(
                hit_data.hit_attr.boost_by_hp for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
            )
            if crisis_available:
                cond_elems.append({(buff_cond,) for buff_cond in ConditionCategories.self_hp_status.members})

        # Buff boosts available
        boost_by_buff_available: bool = any(
            hit_data.hit_attr.boost_by_buff_count
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        buff_up_bonus_hits_available: bool = any(
            hit_data.is_depends_on_user_buff_count
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        if boost_by_buff_available:
            # Add direct boost conditions (only add the sectioned buff count condition if not exporting)
            if not is_exporting:
                cond_elems.append({(buff_cond,) for buff_cond in ConditionCategories.self_buff_count.members})

            # Check if any buff boost data available
            buff_boost_data_ids: set[int] = {hit_data.hit_attr.buff_boost_data_id
                                             for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv} - {0}
            if buff_boost_data_ids:
                # Buff boost data available, check all buff boost data and add its related condition
                for buff_boost_data_id in buff_boost_data_ids:
                    buff_boost_data = self.asset_manager.asset_buff_count.get_data_by_id(buff_boost_data_id)
                    action_condition_id = buff_boost_data.action_condition_id

                    cond_elems.append({
                        (buff_cond,) for buff_cond
                        in ConditionCategories.get_category_action_condition(action_condition_id).members
                    })
        elif buff_up_bonus_hits_available:
            # Get all action IDs first, then get the max bullet counts
            # to reduce the call count of getting the action info
            action_ids = {hit_data.action_id for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv}
            max_count: int = max(
                self.asset_manager.asset_action_info_player.get_data_by_id(action_id).max_bullet_count
                for action_id in action_ids
            )
            cond_elems.append({
                (buff_cond,) for buff_cond
                in ConditionCategories.self_buff_count.get_members_lte(max_count)
            })

        return cond_elems

    def _init_all_possible_conditions_self_others(self, is_exporting: bool):
        cond_elems: list[set[tuple[Condition, ...]]] = []

        # Combo boosts available
        combo_boost_conditions: set[Condition, ...] = {
            combo_condition
            for hit_data_lv in self.hit_data_mtx
            for hit_data in hit_data_lv
            for combo_condition in hit_data.boost_by_combo_conditions
        }
        if combo_boost_conditions:
            # Combo conditions in hit data may not have combo 0 as condition
            combo_boost_conditions.add(Condition.COMBO_GTE_0)
            cond_elems.append({(combo_cond,) for combo_cond in combo_boost_conditions})

        # Gauge boosts available
        gauge_boost_available: bool = any(
            hit_data.is_boost_by_gauge_filled for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        if gauge_boost_available:
            cond_elems.append({(combo_cond,) for combo_cond in ConditionCategories.self_gauge_filled.members})

        # In buff field boosts available
        if not is_exporting and any(
                hit_data.is_effective_inside_buff_field
                for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        ):
            cond_elems.append({(buff_cond,) for buff_cond in ConditionCategories.self_in_buff_field_self.members})
            cond_elems.append({(buff_cond,) for buff_cond in ConditionCategories.self_in_buff_field_ally.members})

        return cond_elems

    def _init_all_possible_conditions_skill(self):
        cond_elems: list[set[tuple[Condition, ...]]] = []

        # Teammate coverage available
        teammate_coverage_available: bool = any(
            hit_data.hit_attr.has_hit_condition for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        if teammate_coverage_available:
            cond_elems.append({
                (teammate_coverage,) for teammate_coverage in ConditionCategories.skill_teammates_covered.members
            })

        # Deterioration available
        will_deteriorate: bool = any(
            hit_data.will_deteriorate for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        if will_deteriorate:
            max_bullet_hit: int = max(
                (hit_data.max_hit_count for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv)
            )
            cond_elems.append({
                (bullet_hit,) for bullet_hit
                in ConditionCategories.skill_bullet_hit.get_members_lte(max_bullet_hit)
            })

        # Bullet summon count dependent & available
        depends_on_bullet_summoned: int = max(
            (hit_data.is_depends_on_bullet_summoned for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv)
        )
        if depends_on_bullet_summoned:
            # EXNOTE: Only Naveed uses this as of 2020/12/11.
            max_bullet_hit: int = max(
                (hit_data.max_hit_count for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv)
            )
            cond_elems.append({
                (bullet_on_map,) for bullet_on_map
                in ConditionCategories.skill_bullets_on_map.get_members_lte(max_bullet_hit)
            })

        # On-map bullet count dependent & available
        depends_on_bullets_on_map: int = max(
            (hit_data.is_depends_on_bullet_on_map for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv)
        )
        if depends_on_bullets_on_map:
            # EXNOTE: Only Meene uses this as of 2020/12/11.
            #   This has a limitation of the 9 butterflies limitation (not yet implemented).
            #   The parser uses the limited enums to do the limitating work for now.
            cond_elems.append({
                (bullet_on_map,) for bullet_on_map in ConditionCategories.skill_bullets_on_map.members
            })

        return cond_elems

    def _init_all_possible_conditions(self, /, is_exporting: bool):
        # Initialization
        cond_elems: list[set[tuple[Condition, ...]]] = self._init_possible_conditions_base_elems()

        cond_elems.extend(self._init_all_possible_conditions_target())
        cond_elems.extend(self._init_all_possible_conditions_self_crisis_buff(is_exporting))
        cond_elems.extend(self._init_all_possible_conditions_self_others(is_exporting))
        cond_elems.extend(self._init_all_possible_conditions_skill())

        # Add combinations
        self.possible_conditions = {
            ConditionComposite(tuple(subitem for item in item_combination for subitem in item))
            for item_combination in product(*cond_elems)
        }

    def _init_buff_field_boost_mtx(self):
        self._buff_field_boost_mtx = [
            BuffFieldBoostData.from_hit_units(hit_data_lv)
            for hit_data_lv in self.hit_data_mtx
        ]

    def _init_max_level(self, *args, **kwargs) -> int:
        # Calculate the max level by getting the level which has the max total mods
        # -------------------------------------------------------------------------
        # Some dummy data were inserted for a higher (& usually unreleased) level,
        # causing the max level to be inaccurate if we simply get the length of the mods matrix.
        #
        # If there are 2 levels sharing the same total mods, the higher level will be used.
        return max(zip(reversed([sum(unit.mod for unit in units) for units in self._unit_mtx_base]),
                       range(len(self._unit_mtx_base), 0, -1)),
                   key=lambda item: item[0])[1]

    def __post_init__(self, is_exporting: bool):
        # Initialize here despite `__post_init__` assigns it
        # because this property is used in `calculate_units_matrix`
        self.hit_data_mtx = self.skill_hit_data.hit_data
        # This need to be placed before `__post_init__`
        # because `self._unit_mtx_base` is used to determine the skill max level
        self._unit_mtx_base, _ = self.calculate_units_matrix(ConditionComposite())

        super().__post_init__(is_exporting=is_exporting)

        self._init_buff_field_boost_mtx()

        self.cancel_unit_mtx_base = self.skill_hit_data.cancel_unit_mtx

        self._has_non_zero_mods = any(
            sum(unit.mod for unit in units) > 0
            for entry in self.get_all_possible_entries()
            for units in entry.hit_unit_mtx
        )

    def calculate_units_matrix(
            self, condition_comp: ConditionComposite, action_id: Optional[int] = None,
    ) -> tuple[list[list[DamageUnit]], list[int]]:
        """Calculate the damage unit matrix and the hit count vector."""
        units: list[list[DamageUnit]] = []
        action_id_mtx: list[set[int]] = []
        hit_counts: list[int] = []

        if not condition_comp:
            condition_comp = ConditionComposite()  # Dummy empty condition composite

        for hit_data_lv in self.hit_data_mtx:
            new_units_level = []  # Array of the units at the same level
            new_action_ids_level = set()
            # Hit counter for the damage unit calculation (Nadine S1 teammate coverage handling)
            new_units_hit_counter = 0
            # Hit counter for the conditional hits by hit count
            # The count of this will not be used for each damage unit calculation,
            # but will be used after parsing all damage units to get the actual hit count
            new_units_hit_counter_exclusive = 0

            for hit_data in hit_data_lv:
                if action_id and action_id != hit_data.action_id:
                    continue  # Skip processing if the action ID of `hit_data` is not the desired one

                damage_units = hit_data.to_damage_units(
                    condition_comp, new_units_hit_counter, asset_manager=self.asset_manager
                )

                new_units_level.append(damage_units)
                if damage_units:  # Only add action IDs if damage unit is not an empty array
                    new_action_ids_level.add(hit_data.action_id)

                # Add hit count according to the count of damage units that actually deals damage
                # -------------------------------------------------------------------------------
                # Filters delayed damage (for example, mark explosion)
                # Increases different counter according to the hit flag of hit condition
                unit_hit_count = len([unit for unit in damage_units if unit.mod])
                if not hit_data.hit_attr.has_hit_condition:
                    new_units_hit_counter += unit_hit_count
                else:
                    new_units_hit_counter_exclusive += unit_hit_count

                # Add dummy hit counts according to the teammate coverage
                # Do **NOT** use ``damage_units`` for counting the dummy hits because
                # ``damage_units`` is an empty list when ``hit_data`` only deals dummy hits
                new_units_hit_counter += (hit_data.hit_attr.dummy_hit_count
                                          * ((condition_comp.teammate_coverage_converted or 0) + 1))

            # "Flatten" the damage units matrix
            # ---------------------------------
            # For deteriorating bullets:
            # [[1, 0.5, 0.2], [1, 0.5, 0.2]] needs to be transformed to [1, 1, 0.5, 0.5, 0.2, 0.2]
            # For Nevin S2 @ Sigil Released:
            # [[9], [0.9, 0.9]] needs to be transformed to [9, 0.9, 0.9]
            units.append([
                subitem for item in zip_longest(*new_units_level, fillvalue=None)
                for subitem in item if subitem  # `if subitem` for filtering `None`
            ])
            action_id_mtx.append(new_action_ids_level)
            # Add the hit counters
            hit_counts.append(new_units_hit_counter + new_units_hit_counter_exclusive)

        self.check_unchained_action_ids_at_same_level(action_id_mtx)

        return units, hit_counts

    def get_cancel_unit_mtx(self, condition_comp: ConditionComposite) -> list[list[SkillCancelActionUnit]]:
        """Get the filtered cancel unit matrix according to ``condition_comp``."""
        ret = []

        for units_lv in self.cancel_unit_mtx_base:
            ret.append([cancel_unit for cancel_unit in units_lv if cancel_unit.pre_conditions in condition_comp])

        return ret

    def with_conditions(
            self, condition_comp: ConditionComposite = None, *, action_id: Optional[int] = None
    ) -> AttackingSkillDataEntry:
        """
        Get the skill data when all conditions in ``condition_comp`` hold.

        If ``condition_comp`` are not given, base data will be returned.

        If there are multiple actions sharing the same condition, ``action_id`` must be specified.
        Otherwise, :class:`MultipleActionsError` will be raised.

        :raises ConditionValidationFailedError: if the condition combination is invalid
        :raises BulletEndOfLifeError: if the bullet hit count condition is beyond the limit
        :raises MultipleActionsError: if there are multiple actions sharing the same condition
        """
        if not condition_comp:
            condition_comp = ConditionComposite()

        hit_unit_mtx, hit_count_vct = self.calculate_units_matrix(condition_comp, action_id)

        return AttackingSkillDataEntry(
            asset_action_cond=self.asset_manager.asset_action_cond,
            asset_buff_count=self.asset_manager.asset_buff_count,
            buff_field_boost_mtx=self._buff_field_boost_mtx,
            condition_comp=condition_comp,
            hit_unit_mtx=hit_unit_mtx,
            cancel_unit_mtx=self.get_cancel_unit_mtx(condition_comp),
            hit_count=hit_count_vct,
            max_level=self.max_level
        )

    @property
    def has_non_zero_mods(self) -> bool:
        """Check if the skill data has at least one damage modifier > 0 hit at any level."""
        return self._has_non_zero_mods
