"""Conditions for the skill data entries."""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Iterable, Sequence, Union

from dlparse.errors import EnumConversionError, ConditionValidationFailedError
from .affliction import Affliction
from .condition_base import ConditionCompositeBase, ConditionCheckResultMixin
from .element import Element

__all__ = ("SkillCondition", "SkillConditionCheckResult", "SkillConditionComposite")


class SkillConditionCheckResult(ConditionCheckResultMixin, Enum):
    """Skill conditions validating result."""

    PASS = auto()

    MULTIPLE_HP = auto()
    MULTIPLE_BUFF = auto()
    MULTIPLE_BULLET_HIT = auto()
    MULTIPLE_TEAMMATE_COVERAGE = auto()
    MULTIPLE_TARGET_ELEMENT = auto()

    INTERNAL_NOT_AFFLICTION_ONLY = auto()
    INTERNAL_NOT_BUFF_COUNT = auto()
    INTERNAL_NOT_BULLET_HIT_COUNT = auto()
    INTERNAL_NOT_HP_CONDITION = auto()
    INTERNAL_NOT_TEAMMATE_COVERAGE = auto()
    INTERNAL_NOT_TARGET_ELEMENTAL = auto()

    @classmethod
    def passing_enums(cls) -> set["SkillConditionCheckResult"]:
        return {cls.PASS}


class SkillCondition(Enum):
    """
    Conditions for the skill data entries.

    .. note::
        Check https://github.com/PyCQA/pylint/issues/2306 for the reason of
        enum values being casted in the categorical check, although redundant.
    """

    NONE = 0

    # region Target
    # region Afflicted
    TARGET_POISONED = 101
    TARGET_BURNED = 102
    TARGET_FROZEN = 103
    TARGET_PARALYZED = 104
    TARGET_BLINDED = 105
    TARGET_STUNNED = 106
    TARGET_CURSED = 107
    TARGET_BOGGED = 109
    TARGET_SLEPT = 110
    TARGET_FROSTBITTEN = 111
    TARGET_FLASHBURNED = 112
    TARGET_CRASHWINDED = 113
    TARGET_SHADOWBLIGHTED = 114
    # endregion

    # region Elemental
    TARGET_ELEM_FLAME = 151
    TARGET_ELEM_WATER = 152
    TARGET_ELEM_WIND = 153
    TARGET_ELEM_LIGHT = 154
    TARGET_ELEM_SHADOW = 155
    # endregion
    # endregion

    # region Self status
    # region HP
    SELF_HP_1 = 201
    SELF_HP_FULL = 202
    # endregion

    # region Buff count
    SELF_BUFF_0 = 251
    SELF_BUFF_10 = 252
    SELF_BUFF_20 = 253
    SELF_BUFF_25 = 254
    SELF_BUFF_30 = 255
    SELF_BUFF_35 = 256
    SELF_BUFF_40 = 257
    SELF_BUFF_45 = 258
    SELF_BUFF_50 = 259
    # endregion
    # endregion

    # region Skill animation/effect
    # region Bullet hit count
    BULLET_HIT_1 = 301
    BULLET_HIT_2 = 302
    BULLET_HIT_3 = 303
    BULLET_HIT_4 = 304
    BULLET_HIT_5 = 305
    BULLET_HIT_6 = 306
    BULLET_HIT_7 = 307
    BULLET_HIT_8 = 308
    BULLET_HIT_9 = 309
    BULLET_HIT_10 = 310
    # endregion

    # region Count of teammates covered
    COVER_TEAMMATE_0 = 351
    COVER_TEAMMATE_1 = 352
    COVER_TEAMMATE_2 = 353
    COVER_TEAMMATE_3 = 354

    # endregion
    # endregion

    @property
    def is_target_afflicted(self) -> bool:
        """If the condition needs the target to be afflicted."""
        return 100 <= int(self.value) <= 150

    @property
    def is_target_elemental(self):
        """If the condition needs the target to be a certain element."""
        return 150 <= int(self.value) <= 159

    @property
    def is_hp_condition(self) -> bool:
        """If the condition is a HP condition."""
        return self in (self.SELF_HP_1, self.SELF_HP_FULL)

    @property
    def is_buff_boost(self) -> bool:
        """If the condition is a buff boosted condition."""
        return 250 <= int(self.value) <= 269

    @property
    def is_bullet_hit_count(self):
        """If the condition is bullet hit count."""
        return 301 <= int(self.value) <= 310

    @property
    def is_teammate_coverage(self):
        """If the condition is teammate coverage."""
        return 351 <= int(self.value) <= 360

    def to_affliction(self) -> Affliction:
        """
        Convert this :class:`SkillCondition` to :class:`Affliction`.

        :raises EnumConversionError: skill condition cannot be converted to affliction
        """
        if self not in TRANS_DICT_TO_AFFLICTION:
            raise EnumConversionError(self, self.__class__, Affliction)

        return TRANS_DICT_TO_AFFLICTION[self]

    def to_buff_count(self) -> int:
        """
        Convert this :class:`SkillCondition` to the actual count of buffs.

        :raises EnumConversionError: skill condition cannot be converted to buff count
        """
        if self not in TRANS_DICT_TO_BUFF_COUNT:
            raise EnumConversionError(self, self.__class__, "buff count")

        return TRANS_DICT_TO_BUFF_COUNT[self]

    def to_bullet_hit_count(self) -> int:
        """
        Convert this :class:`SkillCondition` to the actual count of bullet hits.

        :raises EnumConversionError: skill condition cannot be converted to bullet hit count
        """
        if self not in TRANS_DICT_TO_BULLET_HIT_COUNT:
            raise EnumConversionError(self, self.__class__, "bullet hit count")

        return TRANS_DICT_TO_BULLET_HIT_COUNT[self]

    def to_teammate_coverage_count(self) -> int:
        """
        Convert this :class:`SkillCondition` to the actual count of teammates covered.

        :raises EnumConversionError: skill condition cannot be converted to count of teammates covered
        """
        if self not in TRANS_DICT_TO_TEAMMATE_COUNT:
            raise EnumConversionError(self, self.__class__, "count of teammates covered")

        return TRANS_DICT_TO_TEAMMATE_COUNT[self]

    def to_element(self) -> Element:
        """
        Convert this :class:`SkillCondition` to :class:`Element`.

        :raises EnumConversionError: skill condition cannot be converted to element enum
        """
        if self not in TRANS_DICT_TO_ELEMENT:
            raise EnumConversionError(self, self.__class__, "element")

        return TRANS_DICT_TO_ELEMENT[self]

    @staticmethod
    def get_buff_count_conditions() -> list["SkillCondition"]:
        """Get a list of all buff count conditions."""
        return list(TRANS_DICT_TO_BUFF_COUNT.keys())

    @staticmethod
    def get_bullet_hit_count_conditions(max_count: int) -> list["SkillCondition"]:
        """Get a list of bullet hit count conditions which is <= ``max_count``."""
        return [cond_enum for cond_enum, hit_count in TRANS_DICT_TO_BULLET_HIT_COUNT.items()
                if hit_count <= max_count]

    @staticmethod
    def get_teammate_coverage_conditions() -> list["SkillCondition"]:
        """Get all teammate coverage conditions."""
        return list(TRANS_DICT_TO_TEAMMATE_COUNT.keys())

    @staticmethod
    def get_teammate_coverage_counts() -> list[int]:
        """Get all available teammate coverage counts."""
        return list(TRANS_DICT_TO_TEAMMATE_COUNT.values())

    @staticmethod
    def extract_afflictions(conditions: Sequence["SkillCondition"]) -> set["SkillCondition"]:
        """
        Get a list of affliction conditions from ``conditions``.

        Returns an empty set if not found.
        """
        return {condition for condition in conditions if condition.is_target_afflicted}

    @staticmethod
    def extract_buff_count(conditions: Sequence["SkillCondition"]) -> Optional["SkillCondition"]:
        """
        Get the first buff count condition from ``conditions``, if found.

        Returns ``None`` instead if not found.

        This will **NOT** throw an error if there are multiple buff conditions found.
        """
        return next((condition for condition in conditions if condition.is_buff_boost), None)

    @staticmethod
    def extract_bullet_hit_count(conditions: Sequence["SkillCondition"]) -> Optional["SkillCondition"]:
        """
        Get the first bullet hit count condition from ``conditions``, if found.

        Returns ``None`` instead if not found.

        This will **NOT** throw an error if there are multiple bullet count conditions found.
        """
        return next((condition for condition in conditions if condition.is_bullet_hit_count), None)

    @staticmethod
    def extract_hp_condition(conditions: Sequence["SkillCondition"]) -> Optional["SkillCondition"]:
        """
        Get the first HP condition from ``conditions``, if found.

        Returns ``None`` instead if not found.

        This will **NOT** throw an error if there are multiple HP conditions found.
        """
        return next((condition for condition in conditions if condition.is_hp_condition), None)

    @staticmethod
    def extract_teammate_coverage(conditions: Sequence["SkillCondition"]) -> Optional["SkillCondition"]:
        """
        Get the teammate coverage condition from ``conditions``, if found.

        Returns ``None`` instead if not found.

        This will **NOT** throw an error if there are multiple teammate coverage conditions found.
        """
        return next((condition for condition in conditions if condition.is_teammate_coverage), None)

    @staticmethod
    def extract_target_elemental(conditions: Sequence["SkillCondition"]) -> Optional["SkillCondition"]:
        """
        Get the target element condition from ``conditions``, if found.

        Returns ``None`` instead if not found.

        This will **NOT** throw an error if there are multiple target element conditions found.
        """
        return next((condition for condition in conditions if condition.is_target_elemental), None)

    @staticmethod
    def from_affliction(affliction: Affliction) -> "SkillCondition":
        """
        Convert ``affliction`` to :class:`SkillCondition`.

        :raises EnumConversionError: affliction cannot be converted to skill condition
        """
        if affliction not in TRANS_DICT_FROM_AFFLICTION:
            raise EnumConversionError(affliction, Affliction, SkillCondition)

        return TRANS_DICT_FROM_AFFLICTION[affliction]

    @staticmethod
    def validate_conditions(conditions: Optional[Iterable["SkillCondition"]] = None) -> SkillConditionCheckResult:
        """
        Check the validity of ``conditions``.

        If any of the following holds, conditions are considered invalid.

        - Multiple HP conditions exist.

        - Multiple buff count exist.

        - Multiple bullet hit count exist.
        """
        # No conditions given
        if not conditions:
            return SkillConditionCheckResult.PASS

        # Multiple HP check
        if sum(condition.is_hp_condition for condition in conditions) > 1:
            return SkillConditionCheckResult.MULTIPLE_HP

        # Multiple buff check
        if sum(condition.is_buff_boost for condition in conditions) > 1:
            return SkillConditionCheckResult.MULTIPLE_BUFF

        # Multiple bullet hit count check
        if sum(condition.is_bullet_hit_count for condition in conditions) > 1:
            return SkillConditionCheckResult.MULTIPLE_BULLET_HIT

        # Teammate coverage condition check
        if sum(condition.is_teammate_coverage for condition in conditions) > 1:
            return SkillConditionCheckResult.MULTIPLE_TEAMMATE_COVERAGE

        # Target element condition check
        if sum(condition.is_target_elemental for condition in conditions) > 1:
            return SkillConditionCheckResult.MULTIPLE_TARGET_ELEMENT

        return SkillConditionCheckResult.PASS


@dataclass(eq=False)  # ``eq=False`` to keep the superclass ``__hash__``
class SkillConditionComposite(ConditionCompositeBase[SkillCondition]):
    """Composite class of various attacking skill conditions."""

    afflictions_condition: set[SkillCondition] = field(init=False)
    afflictions_converted: set[Affliction] = field(init=False)
    buff_count: Optional[SkillCondition] = field(init=False)
    bullet_hit_count: Optional[SkillCondition] = field(init=False)
    hp_condition: Optional[SkillCondition] = field(init=False)
    teammate_coverage: Optional[SkillCondition] = field(init=False)
    target_elemental: Optional[SkillCondition] = field(init=False)

    @staticmethod
    def _init_validate_conditions(conditions: tuple[SkillCondition]):
        # Validate the condition combinations
        # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
        if not (result := SkillCondition.validate_conditions(conditions)):  # pylint: disable=superfluous-parens
            raise ConditionValidationFailedError(result)

    def _init_validate_fields(self):
        # Check `self.afflictions_condition`
        if any(not condition.is_target_afflicted for condition in self.afflictions_condition):
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_AFFLICTION_ONLY)

        # Check `self.buff_count`
        if self.buff_count and not self.buff_count.is_buff_boost:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_BUFF_COUNT)

        # Check `self.bullet_hit_count`
        if self.bullet_hit_count and not self.bullet_hit_count.is_bullet_hit_count:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_BULLET_HIT_COUNT)

        # Check `self.hp_condition`
        if self.hp_condition and not self.hp_condition.is_hp_condition:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_HP_CONDITION)

        # Check `self.teammate_coverage`
        if self.teammate_coverage and not self.teammate_coverage.is_teammate_coverage:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_TEAMMATE_COVERAGE)

        # Check `self.target_elemental`
        if self.target_elemental and not self.target_elemental.is_target_elemental:
            raise ConditionValidationFailedError(SkillConditionCheckResult.INTERNAL_NOT_TARGET_ELEMENTAL)

    def __post_init__(self, conditions: Optional[Union[Sequence[SkillCondition], SkillCondition]]):
        conditions = self._init_process_conditions(conditions)

        self.afflictions_condition = SkillCondition.extract_afflictions(conditions)
        self.buff_count = SkillCondition.extract_buff_count(conditions)
        self.bullet_hit_count = SkillCondition.extract_bullet_hit_count(conditions)
        self.hp_condition = SkillCondition.extract_hp_condition(conditions)
        self.teammate_coverage = SkillCondition.extract_teammate_coverage(conditions)
        self.target_elemental = SkillCondition.extract_target_elemental(conditions)

        self._init_validate_fields()

        self.afflictions_converted = {condition.to_affliction() for condition in self.afflictions_condition}

    @property
    def conditions_sorted(self) -> tuple[SkillCondition]:
        """
        Get the sorted conditions as a tuple.

        Conditions will be sorted in the following order:

        - Afflictions
        - Target element
        - HP
        - Buff count
        - Bullet hit count
        - Teammate coverage
        """
        ret: tuple[SkillCondition] = tuple(self.afflictions_condition)

        if self.target_elemental:
            ret += (self.target_elemental,)

        if self.hp_condition:
            ret += (self.hp_condition,)

        if self.buff_count:
            ret += (self.buff_count,)

        if self.bullet_hit_count:
            ret += (self.bullet_hit_count,)

        if self.teammate_coverage:
            ret += (self.teammate_coverage,)

        return ret


TRANS_DICT_TO_AFFLICTION: dict[SkillCondition, Affliction] = {
    SkillCondition.TARGET_POISONED: Affliction.POISON,
    SkillCondition.TARGET_BURNED: Affliction.BURN,
    SkillCondition.TARGET_FROZEN: Affliction.FREEZE,
    SkillCondition.TARGET_PARALYZED: Affliction.PARALYZE,
    SkillCondition.TARGET_BLINDED: Affliction.BLIND,
    SkillCondition.TARGET_STUNNED: Affliction.STUN,
    SkillCondition.TARGET_CURSED: Affliction.CURSE,
    SkillCondition.TARGET_BOGGED: Affliction.BOG,
    SkillCondition.TARGET_SLEPT: Affliction.SLEEP,
    SkillCondition.TARGET_FROSTBITTEN: Affliction.FROSTBITE,
    SkillCondition.TARGET_FLASHBURNED: Affliction.FLASHBURN,
    SkillCondition.TARGET_CRASHWINDED: Affliction.CRASHWIND,
    SkillCondition.TARGET_SHADOWBLIGHTED: Affliction.SHADOWBLIGHT,
}
"""A :class:`dict` to convert :class:`SkillCondition` to :class:`Affliction`."""

TRANS_DICT_FROM_AFFLICTION: dict[Affliction, SkillCondition] = {
    Affliction.POISON: SkillCondition.TARGET_POISONED,
    Affliction.BURN: SkillCondition.TARGET_BURNED,
    Affliction.FREEZE: SkillCondition.TARGET_FROZEN,
    Affliction.PARALYZE: SkillCondition.TARGET_PARALYZED,
    Affliction.BLIND: SkillCondition.TARGET_BLINDED,
    Affliction.STUN: SkillCondition.TARGET_STUNNED,
    Affliction.CURSE: SkillCondition.TARGET_CURSED,
    Affliction.BOG: SkillCondition.TARGET_BOGGED,
    Affliction.SLEEP: SkillCondition.TARGET_SLEPT,
    Affliction.FROSTBITE: SkillCondition.TARGET_FROSTBITTEN,
    Affliction.FLASHBURN: SkillCondition.TARGET_FLASHBURNED,
    Affliction.CRASHWIND: SkillCondition.TARGET_CRASHWINDED,
    Affliction.SHADOWBLIGHT: SkillCondition.TARGET_SHADOWBLIGHTED,
}
"""A :class:`dict` to convert :class:`Affliction` to :class:`SkillCondition`."""

TRANS_DICT_TO_BUFF_COUNT: dict[SkillCondition, int] = {
    SkillCondition.SELF_BUFF_0: 0,
    SkillCondition.SELF_BUFF_10: 10,
    SkillCondition.SELF_BUFF_20: 20,
    SkillCondition.SELF_BUFF_25: 25,
    SkillCondition.SELF_BUFF_30: 30,
    SkillCondition.SELF_BUFF_35: 35,
    SkillCondition.SELF_BUFF_40: 40,
    SkillCondition.SELF_BUFF_45: 45,
    SkillCondition.SELF_BUFF_50: 50,
}
"""A :class:`dict` to convert :class:`SkillCondition` to the number of buff counts."""

TRANS_DICT_TO_BULLET_HIT_COUNT: dict[SkillCondition, int] = {
    SkillCondition.BULLET_HIT_1: 1,
    SkillCondition.BULLET_HIT_2: 2,
    SkillCondition.BULLET_HIT_3: 3,
    SkillCondition.BULLET_HIT_4: 4,
    SkillCondition.BULLET_HIT_5: 5,
    SkillCondition.BULLET_HIT_6: 6,
    SkillCondition.BULLET_HIT_7: 7,
    SkillCondition.BULLET_HIT_8: 8,
    SkillCondition.BULLET_HIT_9: 9,
    SkillCondition.BULLET_HIT_10: 10,
}
"""A :class:`dict` to convert :class:`SkillCondition` to the number of bullet hit counts."""

TRANS_DICT_TO_TEAMMATE_COUNT: dict[SkillCondition, int] = {
    SkillCondition.COVER_TEAMMATE_0: 0,
    SkillCondition.COVER_TEAMMATE_1: 1,
    SkillCondition.COVER_TEAMMATE_2: 2,
    SkillCondition.COVER_TEAMMATE_3: 3,
}
"""A :class:`dict` to convert :class:`SkillCondition` to the number of teammates covered."""

TRANS_DICT_TO_ELEMENT: dict[SkillCondition, Element] = {
    SkillCondition.TARGET_ELEM_FLAME: Element.FLAME,
    SkillCondition.TARGET_ELEM_WATER: Element.WATER,
    SkillCondition.TARGET_ELEM_WIND: Element.WIND,
    SkillCondition.TARGET_ELEM_LIGHT: Element.LIGHT,
    SkillCondition.TARGET_ELEM_SHADOW: Element.SHADOW,
}
"""A :class:`dict` to convert :class:`SkillCondition` to the corresponding :class:`Element`."""
