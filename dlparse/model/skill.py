"""Models for character skills."""
from dataclasses import dataclass, field
from itertools import combinations, product
from typing import Optional, Union, Sequence

from dlparse.enums import SkillCondition, Affliction
from dlparse.errors import ConditionValidationFailedError
from dlparse.mono.asset import HitAttrEntry, SkillDataEntry

__all__ = ("AttackingSkillDataEntry", "AttackingSkillData")


@dataclass
class AttackingSkillDataEntry:
    """
    An entry of the attacking skill data.

    Both ``hit_count`` and ``mods`` should be sorted by the skill level.

    For example, if skill level 1 has 1 hit and 100% mods while skill level 2 has 2 hits and 150% + 200% mods,
    ``hit_count`` should be ``[1, 2]`` and ``mods`` should be ``[[1.0], [1.5, 2.0]]``.

    To apply the data of the entry, **all** ``conditions`` must be true.
    """

    hit_count: list[int]
    mods: list[list[float]]

    damage_hit_attrs: list[list[HitAttrEntry]]

    conditions: tuple[SkillCondition] = field(default_factory=tuple)

    total_mod: list[float] = field(init=False)

    def __post_init__(self):
        self.total_mod = [sum(mods) for mods in self.mods]

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

    hit_count: list[int]
    mods: list[list[float]]

    hit_attr_mtx: list[list[HitAttrEntry]]

    possible_conditions: set[tuple[SkillCondition]] = field(init=False)
    """
    All possible combination of the conditions.

    This will be sorted in the order of:

    - HP
    - Buff count
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

        # Check availabilities
        for hit_attrs in self.hit_attr_mtx:
            for hit_attr in hit_attrs:
                punishers_available.update(hit_attr.punisher_states)
                crisis_available = crisis_available or hit_attr.change_by_hp
                buff_up_available = buff_up_available or hit_attr.boost_by_buff_count

        cond_elems: list[set[tuple[SkillCondition, ...]]] = []

        # Crisis boosts available, attach HP conditions
        if crisis_available:
            cond_elems.append({(SkillCondition.SELF_HP_1,), (SkillCondition.SELF_HP_FULL,)})

        # Buff boosts available, attach buff counts
        if buff_up_available:
            cond_elems.append({(buff_cond,) for buff_cond in SkillCondition.get_all_buff_count_conditions()})

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
        self.possible_conditions = set()
        self._init_all_possible_conditions()

    @staticmethod
    def _validate_conditions(conditions: Optional[Union[Sequence[SkillCondition], SkillCondition]] = None):
        # Validate the condition combinations
        # https://github.com/PyCQA/pylint/issues/3249
        if not (result := SkillCondition.validate_conditions(conditions)):  # pylint: disable=superfluous-parens
            raise ConditionValidationFailedError(result)

    def get_base_entry(self) -> AttackingSkillDataEntry:
        """Get the base skill data entry."""
        self._validate_conditions()

        return AttackingSkillDataEntry(
            hit_count=self.hit_count,
            mods=self.mods,
            damage_hit_attrs=self.hit_attr_mtx,
        )

    def with_conditions(self, conditions: Optional[Union[Sequence[SkillCondition], SkillCondition]] = None) \
            -> AttackingSkillDataEntry:
        """
        Get the skill data when all ``conditions`` match.

        If ``conditions`` are not given, return the base data.

        :raises ConditionValidationFailedError: if the condition combination is invalid

        .. note::
            If there are duplicated buff count ``conditions``, only the first one will be used.

            Hit count could be 0, since a skill may be attacking and supportive combined across the levels
            (OG Elisanne S1 - `105402011`).
        """
        if not conditions:
            # Return the base entry if the conditions are not given, or the conditions will not cause differences
            return self.get_base_entry()

        if isinstance(conditions, SkillCondition):
            # Cast the condition to be a list to generalize the data type
            conditions = (conditions,)
        elif isinstance(conditions, list):
            # Cast the condition to be a tuple (might be :class:`list` when passed in)
            conditions = tuple(conditions)

        self._validate_conditions(conditions)

        new_mods: list[list[float]] = []

        # Pre-check conditions
        afflictions = {condition.to_affliction() for condition in conditions if condition.is_target_afflicted}
        in_crisis = SkillCondition.SELF_HP_1 in conditions
        buff_count_cond = next((condition for condition in conditions if condition.is_buff_boost), None)

        for og_mods, hit_attrs in zip(self.mods, self.hit_attr_mtx):
            new_mods_level = []  # Array of the mods at the same level

            for mod, hit_attr in zip(og_mods, hit_attrs):
                # Apply punisher boosts
                if hit_attr.has_punisher and afflictions & hit_attr.punisher_states:
                    mod *= hit_attr.punisher_rate

                # Apply crisis boosts
                if hit_attr.change_by_hp and in_crisis:
                    mod *= hit_attr.crisis_limit_rate

                # Apply buff boosts
                if hit_attr.boost_by_buff_count and buff_count_cond:
                    mod *= (1 + hit_attr.rate_boost_by_buff * buff_count_cond.to_buff_count())

                new_mods_level.append(mod)  # Add the calculated mod

            new_mods.append(new_mods_level)  # Add the mods of the level

        return AttackingSkillDataEntry(
            hit_count=self.hit_count,
            mods=new_mods,
            damage_hit_attrs=self.hit_attr_mtx,
            conditions=conditions
        )

    def get_all_possible_entries(self) -> list[AttackingSkillDataEntry]:
        """Get all possible skill mod entries."""
        return [self.with_conditions(conditions) for conditions in self.possible_conditions]
