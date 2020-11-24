"""Conditions for the skill data entries."""
from dataclasses import dataclass, InitVar, field
from enum import Enum, auto
from typing import Optional, Iterable, Sequence, Union

from dlparse.errors import EnumConversionError, ConditionValidationFailedError
from .affliction import Affliction

__all__ = ("SkillCondition", "SkillConditionCheckResult", "SkillConditionComposite")


class SkillConditionCheckResult(Enum):
    """Skill conditions validating result."""

    PASS = auto()

    MULTIPLE_HP = auto()
    MULTIPLE_BUFF = auto()
    MULTIPLE_BULLET_HIT = auto()

    INTERNAL_NOT_AFFLICTION_ONLY = auto()
    INTERNAL_NOT_BUFF_COUNT = auto()
    INTERNAL_NOT_BULLET_HIT_COUNT = auto()
    INTERNAL_NOT_HP_CONDITION = auto()

    def __bool__(self):
        return self.passed

    @property
    def passed(self):
        """If the check result means the check has passed."""
        return self == self.PASS


class SkillCondition(Enum):
    """Conditions for the skill data entries."""

    NONE = 0

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

    SELF_HP_1 = 201
    SELF_HP_FULL = 202

    SELF_BUFF_0 = 251
    SELF_BUFF_10 = 252
    SELF_BUFF_20 = 253
    SELF_BUFF_25 = 254
    SELF_BUFF_30 = 255
    SELF_BUFF_35 = 256
    SELF_BUFF_40 = 257
    SELF_BUFF_45 = 258
    SELF_BUFF_50 = 259

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

    @property
    def is_target_afflicted(self) -> bool:
        """If the condition needs the target to be afflicted."""
        # https://github.com/PyCQA/pylint/issues/2306
        return 100 <= int(self.value) <= 199

    @property
    def is_hp_condition(self) -> bool:
        """If the condition is a HP condition."""
        return self in (self.SELF_HP_1, self.SELF_HP_FULL)

    @property
    def is_buff_boost(self) -> bool:
        """If the condition is a buff boosted condition."""
        # https://github.com/PyCQA/pylint/issues/2306
        return 250 <= int(self.value) <= 269

    @property
    def is_bullet_hit_count(self):
        """If the condition is bullet hit count."""
        # https://github.com/PyCQA/pylint/issues/2306
        return 301 <= int(self.value) <= 310

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

    @staticmethod
    def get_all_buff_count_conditions() -> list["SkillCondition"]:
        """Get a list of all buff count conditions."""
        return list(TRANS_DICT_TO_BUFF_COUNT.keys())

    @staticmethod
    def get_all_bullet_hit_count_conditions() -> list["SkillCondition"]:
        """Get a list of all bullet hit count conditions."""
        return list(TRANS_DICT_TO_BULLET_HIT_COUNT.keys())

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

        return SkillConditionCheckResult.PASS


@dataclass
class SkillConditionComposite:
    """Composite class of various skill conditions."""

    conditions: InitVar[Optional[Union[Sequence[SkillCondition], SkillCondition]]] = None

    afflictions_condition: set[SkillCondition] = field(init=False)
    afflictions_converted: set[Affliction] = field(init=False)
    buff_count: Optional[SkillCondition] = field(init=False)
    bullet_hit_count: Optional[SkillCondition] = field(init=False)
    hp_condition: Optional[SkillCondition] = field(init=False)

    @staticmethod
    def _init_process_conditions(conditions: Optional[Union[Sequence[SkillCondition], SkillCondition]]):
        if isinstance(conditions, SkillCondition):
            # Cast the condition to be a list to generalize the data type
            conditions = (conditions,)
        elif isinstance(conditions, list):
            # Cast the condition to be a tuple (might be :class:`list` when passed in)
            conditions = tuple(conditions)
        elif not conditions:
            # Conditions is either empty sequence or ``None``
            conditions = ()

        return conditions

    @staticmethod
    def _init_validate_conditions(conditions: Optional[Union[Sequence[SkillCondition], SkillCondition]]):
        # Validate the condition combinations
        # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
        if not (result := SkillCondition.validate_conditions(conditions)):  # pylint: disable=superfluous-parens
            raise ConditionValidationFailedError(result)

    def _init_validate(self):
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

    def __post_init__(self, conditions: Optional[Union[Sequence[SkillCondition], SkillCondition]]):
        conditions = self._init_process_conditions(conditions)
        self._init_validate_conditions(conditions)

        self.afflictions_condition = SkillCondition.extract_afflictions(conditions)
        self.buff_count = SkillCondition.extract_buff_count(conditions)
        self.bullet_hit_count = SkillCondition.extract_bullet_hit_count(conditions)
        self.hp_condition = SkillCondition.extract_hp_condition(conditions)

        self._init_validate()

        self.afflictions_converted = {condition.to_affliction() for condition in self.afflictions_condition}

    @property
    def conditions_sorted(self) -> tuple[SkillCondition]:
        """
        Get the sorted conditions as a tuple.

        Conditions will be sorted in the following order:

        - Afflictions
        - HP
        - Buff count
        - Bullet hit count
        """
        ret: tuple[SkillCondition] = tuple(self.afflictions_condition)

        if self.hp_condition:
            ret += (self.hp_condition,)

        if self.buff_count:
            ret += (self.buff_count,)

        if self.bullet_hit_count:
            ret += (self.bullet_hit_count,)

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
