"""Models for character skills."""
from dataclasses import dataclass, field
from itertools import combinations, product
from typing import Optional, Union, Sequence

from dlparse.enums import SkillCondition, SkillConditionComposite, Affliction
from dlparse.errors import BulletEndOfLifeError
from dlparse.mono.asset import SkillDataEntry
from dlparse.utils import calculate_damage_modifier
from .hit import DamagingHitData

__all__ = ("AttackingSkillDataEntry", "AttackingSkillData")


@dataclass
class AttackingSkillDataEntry:
    """
    An entry of the attacking skill data.

    Both ``hit_count`` and ``mods`` should be sorted by the skill level.

    For example, if skill level 1 has 1 hit and 100% mods while skill level 2 has 2 hits and 150% + 200% mods,
    ``hit_count`` should be ``[1, 2]`` and ``mods`` should be ``[[1.0], [1.5, 2.0]]``.

    The relationship between the ``conditions`` are **AND**, which means that all conditions must be true.
    """

    mods: list[list[float]]

    damage_hit_attrs: list[list[DamagingHitData]]

    condition_comp: SkillConditionComposite = field(default_factory=SkillConditionComposite)

    hit_count: list[int] = field(init=False)
    total_mod: list[float] = field(init=False)

    def __post_init__(self):
        self.total_mod = [sum(mods) for mods in self.mods]
        self.hit_count = [len(mods) for mods in self.mods]

    @property
    def hit_count_at_max(self) -> int:
        """Get the skill hit count at the max level."""
        return self.hit_count[-1]

    @property
    def total_mod_at_max(self) -> float:
        """Get the total skill modifier at the max level."""
        return self.total_mod[-1]

    @property
    def mods_at_max(self) -> list[float]:
        """Get the skill modifiers at the max level."""
        return self.mods[-1]

    @property
    def max_available_level(self) -> int:
        """
        Get the max available level of a skill.

        This max level does **NOT** reflect the actual max level in-game.
        To get such, character data is needed.
        """
        return len(self.hit_count)


@dataclass
class AttackingSkillData:
    """
    An attacking skill data.

    Skill data under different condition can be generated from this class as :class:`AttackingSkillDataEntry`.
    """

    skill_data_raw: SkillDataEntry

    hit_data_mtx: list[list[DamagingHitData]]

    mods: list[list[float]] = field(init=False)

    possible_conditions: set[tuple[SkillCondition]] = field(init=False, default_factory=set)
    """
    All possible combination of the conditions.

    This will be sorted in the order of:

    - HP
    - Buff count
    - Bullet hit count
    - Affliction punishers

    .. note::
        Conditions do **NOT** have any meanings in terms of the order.
        The reason of making the condition combination a :class:`tuple` is
        to allow the parental set operation to prevent duplicated condition combination.
    """

    def _init_all_possible_conditions(self):
        punishers_available: set[Affliction] = set()  # Punishers available for each skill
        crisis_available: bool = False
        buff_up_available: bool = False
        will_deteriorate: bool = False

        # Check availabilities
        for hit_data_lv in self.hit_data_mtx:
            for hit_data in hit_data_lv:
                punishers_available |= hit_data.hit_attr.punisher_states
                crisis_available = crisis_available or hit_data.hit_attr.change_by_hp
                buff_up_available = buff_up_available or hit_data.hit_attr.boost_by_buff_count
                will_deteriorate = will_deteriorate or hit_data.will_deteriorate

        cond_elems: list[set[tuple[SkillCondition, ...]]] = []

        # Crisis boosts available, attach HP conditions
        if crisis_available:
            cond_elems.append({(SkillCondition.SELF_HP_1,), (SkillCondition.SELF_HP_FULL,)})

        # Buff boosts available, attach buff counts
        if buff_up_available:
            cond_elems.append({(buff_cond,) for buff_cond in SkillCondition.get_all_buff_count_conditions()})

        # Deterioration available, attach bullet hit counts
        if will_deteriorate:
            cond_elems.append({(bullet_hit,) for bullet_hit in SkillCondition.get_all_bullet_hit_count_conditions()})

        # Punishers available, attach punisher conditions
        if punishers_available:
            conditions: set[SkillCondition] = {SkillCondition.from_affliction(affliction)
                                               for affliction in punishers_available}
            # noinspection PyTypeChecker
            affliction_combinations: set[tuple[SkillCondition, ...]] = set()
            for count in range(len(conditions) + 1):
                affliction_combinations.update(combinations(conditions, count))

            cond_elems.append(affliction_combinations)

        # Add combinations
        self.possible_conditions = {tuple(subitem for item in item_combination for subitem in item)
                                    for item_combination in product(*cond_elems)}

    def __post_init__(self):
        self._init_all_possible_conditions()
        self.mods = self.calculate_mods_matrix()

    def calculate_mods_matrix(self, condition_comp: Optional[SkillConditionComposite] = None) -> list[list[float]]:
        """Calculate the damage modifier matrix."""
        mods: list[list[float]] = []

        if not condition_comp:
            condition_comp = SkillConditionComposite()  # Dummy empty condition composite

        for hit_data_lv in self.hit_data_mtx:
            new_mods_level = []  # Array of the mods at the same level

            for hit_data in hit_data_lv:
                # Add the calculated mod(s)
                new_mods_level.append(calculate_damage_modifier(hit_data, condition_comp))

            # [[1, 0.5, 0.2], [1, 0.5, 0.2]] needs to be transformed to [1, 1, 0.5, 0.5, 0.2, 0.2]
            mods.append([subitem for item in zip(*new_mods_level) for subitem in item])

        return mods

    def get_base_entry(self) -> AttackingSkillDataEntry:
        """Get the base skill data entry."""
        return AttackingSkillDataEntry(
            mods=self.mods,
            damage_hit_attrs=self.hit_data_mtx,
        )

    def with_conditions(self, conditions: Optional[Union[Sequence[SkillCondition], SkillCondition]] = None) \
            -> AttackingSkillDataEntry:
        """
        Get the skill data when all ``conditions`` match.

        If ``conditions`` are not given, return the base data.

        :raises ConditionValidationFailedError: if the condition combination is invalid
        :raises BulletEndOfLifeError: if the bullet hit count condition is beyond the limit

        .. note::
            If there are duplicated buff count ``conditions``, only the first one will be used.

            Hit count could be 0, since a skill may be attacking and supportive combined across the levels
            (OG Elisanne S1 - `105402011`).
        """
        if not conditions:
            # Return the base entry if the conditions are not given, or the conditions will not cause differences
            return self.get_base_entry()

        condition_comp = SkillConditionComposite(conditions)

        return AttackingSkillDataEntry(
            mods=self.calculate_mods_matrix(condition_comp),
            damage_hit_attrs=self.hit_data_mtx,
            condition_comp=condition_comp
        )

    def get_all_possible_entries(self) -> list[AttackingSkillDataEntry]:
        """Get all possible skill mod entries."""
        entries = []

        for conditions in self.possible_conditions:
            try:
                entries.append(self.with_conditions(conditions))
            except BulletEndOfLifeError:
                # bullet count in conditions > actual max bullet count
                pass

        return entries
