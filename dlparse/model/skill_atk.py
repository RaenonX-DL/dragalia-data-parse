"""Models for character skills."""
from dataclasses import dataclass, field
from itertools import combinations, product, zip_longest
from typing import Optional

from dlparse.enums import SkillCondition, SkillConditionCategories, SkillConditionComposite, Status
from dlparse.mono.asset import ActionConditionAsset, PlayerActionInfoAsset
from dlparse.utils import calculate_damage_modifier
from .hit_dmg import DamagingHitData
from .skill_affliction import SkillAfflictionUnit
from .skill_base import SkillDataBase, SkillEntryBase

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

    mods: list[list[float]]
    afflictions: list[list[SkillAfflictionUnit]]

    hit_data_mtx: list[list[DamagingHitData]]

    max_level: int

    condition_comp: SkillConditionComposite

    hit_count: list[int] = field(init=False)
    total_mod: list[float] = field(init=False)

    def __post_init__(self):
        self.total_mod = [sum(mods) for mods in self.mods]
        self.hit_count = [len(mods) for mods in self.mods]

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

    # These are used during mods calculation
    asset_action_info: PlayerActionInfoAsset

    # These are used during affliction processing
    asset_action_cond: ActionConditionAsset

    mods: list[list[float]] = field(init=False)
    afflictions: list[list[SkillAfflictionUnit]] = field(init=False)

    _max_level: int = field(init=False)

    def _init_all_possible_conditions(self):
        # Initialization
        cond_elems: list[set[tuple[SkillCondition, ...]]] = self._init_possible_conditions_base_elems()

        # Punishers available
        punishers_available: set[Status] = {
            punisher_state
            for hit_data_lv in self.hit_data_mtx
            for hit_data in hit_data_lv
            for punisher_state in hit_data.hit_attr.punisher_states
        }
        if punishers_available:
            conditions: set[SkillCondition] = {SkillConditionCategories.target_status.convert_reversed(affliction)
                                               for affliction in punishers_available}
            # noinspection PyTypeChecker
            affliction_combinations: set[tuple[SkillCondition, ...]] = set()
            for count in range(len(conditions) + 1):
                affliction_combinations.update(combinations(conditions, count))

            cond_elems.append(affliction_combinations)

        # Crisis boosts available
        crisis_available: bool = any(
            hit_data.hit_attr.boost_by_hp for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        if crisis_available:
            cond_elems.append({(buff_cond,) for buff_cond in SkillConditionCategories.self_hp_status.members})

        # Buff boosts available
        buff_up_available: bool = any(
            hit_data.hit_attr.boost_by_buff_count or hit_data.is_depends_on_user_buff_count
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        if buff_up_available:
            cond_elems.append({(buff_cond,) for buff_cond in SkillConditionCategories.self_buff_count.members})

        # In buff zone boosts available
        in_buff_zone_available: bool = any(
            hit_data.is_effective_inside_buff_zone
            for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        if in_buff_zone_available:
            cond_elems.append({(buff_cond,) for buff_cond in SkillConditionCategories.self_in_buff_zone_self.members})
            cond_elems.append({(buff_cond,) for buff_cond in SkillConditionCategories.self_in_buff_zone_ally.members})

        # Deterioration available
        will_deteriorate: bool = any(
            hit_data.will_deteriorate for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv
        )
        if will_deteriorate:
            max_bullet_hit: int = max(
                (hit_data.max_hit_count for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv)
            )
            cond_elems.append({(bullet_hit,) for bullet_hit
                               in SkillConditionCategories.skill_bullet_hit.get_members_lte(max_bullet_hit)})

        # On-map bullet count dependent & available
        depends_on_bullets_on_map: int = max(
            (hit_data.is_depends_on_bullet_on_map for hit_data_lv in self.hit_data_mtx for hit_data in hit_data_lv)
        )
        if depends_on_bullets_on_map:
            # TODO: This currently works on Meene, who have 9 butterflies limitation.
            #   However, the 9 butterflies limitation are not implemented yet.
            #   The parser uses the limited enums to do the limitating work for now.
            cond_elems.append({(bullet_on_map,)
                               for bullet_on_map in SkillConditionCategories.skill_bullets_on_map.members})

        # Add combinations
        self.possible_conditions = {
            SkillConditionComposite(tuple(subitem for item in item_combination for subitem in item))
            for item_combination in product(*cond_elems)
        }

    def _init_affliction_mtx(self):
        affliction_mtx: list[list[SkillAfflictionUnit]] = []

        for hit_data_lv in self.hit_data_mtx:
            affliction_lv = []

            for hit_data in hit_data_lv:
                if affliction_unit := hit_data.to_affliction_unit(self.asset_action_cond):
                    affliction_lv.append(affliction_unit)

            # Sort afflictions by its time
            affliction_mtx.append(list(sorted(affliction_lv)))

        return affliction_mtx

    def __post_init__(self):
        super().__post_init__()

        self.mods = self.calculate_mods_matrix()
        self.afflictions = self._init_affliction_mtx()

        if not self.mods:
            self._max_level = 0
        else:
            self._max_level = max(zip(reversed([sum(mods) for mods in self.mods]), range(len(self.mods), 0, -1)),
                                  key=lambda item: item[0])[1]

    def calculate_mods_matrix(self, condition_comp: Optional[SkillConditionComposite] = None) -> list[list[float]]:
        """Calculate the damage modifier matrix."""
        mods: list[list[float]] = []

        if not condition_comp:
            condition_comp = SkillConditionComposite()  # Dummy empty condition composite

        for hit_data_lv in self.hit_data_mtx:
            new_mods_level = []  # Array of the mods at the same level

            for hit_data in hit_data_lv:
                # Add the calculated mod(s) only if the mod list is not empty
                # Sometimes this could be an empty list
                #   - hits that only available if inside a buff zone but the skill condition is not in any buff zone
                if damage_mod := calculate_damage_modifier(
                        hit_data, condition_comp, action_info_asset=self.asset_action_info
                ):
                    new_mods_level.append(damage_mod)

            # (Deteriorating bullets)
            # [[1, 0.5, 0.2], [1, 0.5, 0.2]] needs to be transformed to [1, 1, 0.5, 0.5, 0.2, 0.2]
            # (Nevin S2 @ Sigil Released)
            # [[9], [0.9, 0.9]] needs to be transformed to [9, 0.9, 0.9]
            mods.append([subitem for item in zip_longest(*new_mods_level, fillvalue=None)
                         for subitem in item if subitem])

        return mods

    def get_base_entry(self) -> AttackingSkillDataEntry:
        """Get the base skill data entry."""
        return AttackingSkillDataEntry(
            mods=self.mods,
            afflictions=self.afflictions,
            hit_data_mtx=self.hit_data_mtx,
            max_level=self.max_level,
            condition_comp=SkillConditionComposite()
        )

    def with_conditions(self, condition_comp: SkillConditionComposite = None) -> AttackingSkillDataEntry:
        """
        Get the skill data when all conditions in ``condition_comp`` hold.

        If ``condition_comp`` are not given, return the base data.

        :raises ConditionValidationFailedError: if the condition combination is invalid
        :raises BulletEndOfLifeError: if the bullet hit count condition is beyond the limit
        """
        if not condition_comp:
            # Return the base entry if the conditions are not given, or the conditions will not cause differences
            return self.get_base_entry()

        return AttackingSkillDataEntry(
            mods=self.calculate_mods_matrix(condition_comp),
            afflictions=self.afflictions,
            hit_data_mtx=self.hit_data_mtx,
            condition_comp=condition_comp,
            max_level=self.max_level
        )

    @property
    def max_level(self) -> int:
        return self._max_level
