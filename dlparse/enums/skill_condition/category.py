"""Classes for skill condition categories."""
from enum import Enum, auto
from typing import TypeVar, Generic, Iterable, Union

from dlparse.enums import Affliction, Element
from dlparse.enums.condition_base import ConditionCheckResultMixin
from dlparse.errors import EnumConversionError
from .items import SkillCondition

__all__ = ("SkillConditionCheckResult", "SkillConditionCategories", "SkillConditionMaxCount")


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

    HAS_CONDITIONS_LEFT = auto()

    @classmethod
    def passing_enums(cls) -> set["SkillConditionCheckResult"]:
        return {cls.PASS}


class SkillConditionMaxCount(Enum):
    """Maximum count of conditions of a category allowed in a skill condition composite."""

    SINGLE = auto()
    MULTIPLE = auto()


T = TypeVar("T")


class SkillConditionCategory(Generic[T]):
    """A skill condition category."""

    def __init__(self, data: dict[SkillCondition, T], max_count: SkillConditionMaxCount, name: str,
                 result_on_invalid: SkillConditionCheckResult):
        self._members = data
        self._max_count = max_count
        self._name = name
        self._result_on_invalid = result_on_invalid

    def __contains__(self, item):
        if not isinstance(item, SkillCondition):
            return False

        return item in self.members

    @property
    def name(self) -> str:
        """Get the name of the skill condition category."""
        return self._name

    @property
    def members(self) -> set[SkillCondition]:
        """Get all members of this category."""
        return set(self._members.keys())

    @property
    def targets(self) -> set[T]:
        """Get all targets of this category."""
        return set(self._members.values())

    @property
    def conversion_dict(self) -> dict[SkillCondition, T]:
        """Get the dict for the conversion, which the key is :class:`SkillCondition` and the value is its target."""
        return self._members

    @property
    def max_count_allowed(self) -> SkillConditionMaxCount:
        """Get the maximum count of the condition allowed in a single condition composite."""
        return self._max_count

    @property
    def result_on_invalid(self) -> SkillConditionCheckResult:
        """Get the :class:`SkillConditionCheckResult` to return if the validation failed."""
        return self._result_on_invalid

    def convert(self, item: SkillCondition) -> T:
        """
        Convert ``item`` to :class:`T`.

        :raises EnumConversionError: if `item` is unconvertible
        """
        if item not in self:
            raise EnumConversionError(item, SkillCondition, self._name)

        return self._members[item]

    def convert_reversed(self, item: T) -> SkillCondition:
        """
        Convert ``item`` from :class:`T` to :class:`SkillCondition`.

        :raises EnumConversionError: if `item` is unconvertible
        """
        for skill_cond, target in self._members.items():
            if item == target:
                return skill_cond

        raise EnumConversionError(item, item.__class__, self._name)

    def extract(self, conditions: Iterable[SkillCondition]) -> Union[set[SkillCondition], SkillCondition]:
        """
        Extract :class:`SkillCondition` that belongs to this category from ``conditions``.

        Note that this does **NOT** validate ``conditions``, which means that if there are multiple conditions of
        this category exist in ``conditions`` while the maximum allowed count is set to
        ``SkillConditionMaxCount.SINGLE``, **NO** errors will be yielded.

        Instead, this will return the first element discovered. To validate ``conditions``,
        call ``is_valid()`` instead.
        """
        if self.max_count_allowed == SkillConditionMaxCount.SINGLE:
            return next((condition for condition in conditions if condition in self), None)

        return {condition for condition in conditions if condition in self}

    def is_valid(self, conditions: Iterable[SkillCondition]) -> bool:
        """Check if ``conditions`` is valid."""
        if self.max_count_allowed == SkillConditionMaxCount.SINGLE:
            return len(set(conditions) & set(self.members)) <= 1

        return True


class SkillConditionCategoryTargetInt(SkillConditionCategory[int]):
    """A skill condition category which target is :class:`int`."""

    def get_members_lte(self, threshold: int) -> list[SkillCondition]:
        """Get the members which target is less than or equal to ``threshold``."""
        return [cond_enum for cond_enum, target in self._members.items() if target <= threshold]


class SkillConditionCategories:
    """Categories for skill conditions (:class:`SkillCondition`)."""

    # pylint: disable=too-few-public-methods

    target_affliction = SkillConditionCategory[Affliction](
        {
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
        },
        SkillConditionMaxCount.MULTIPLE,
        "Target Affliction",
        SkillConditionCheckResult.PASS  # Impossible to fail (current only invalid reason is multiple conditions)
    )
    target_elemental = SkillConditionCategory[Element](
        {
            SkillCondition.TARGET_ELEM_FLAME: Element.FLAME,
            SkillCondition.TARGET_ELEM_WATER: Element.WATER,
            SkillCondition.TARGET_ELEM_WIND: Element.WIND,
            SkillCondition.TARGET_ELEM_LIGHT: Element.LIGHT,
            SkillCondition.TARGET_ELEM_SHADOW: Element.SHADOW,
        },
        SkillConditionMaxCount.SINGLE,
        "Target element",
        SkillConditionCheckResult.MULTIPLE_TARGET_ELEMENT
    )
    self_hp = SkillConditionCategoryTargetInt(
        {
            SkillCondition.SELF_HP_1: 0,
            SkillCondition.SELF_HP_FULL: 1,
            SkillCondition.SELF_HP_LT_40: 1,
            SkillCondition.SELF_HP_GTE_40: 1,
        },
        SkillConditionMaxCount.SINGLE,
        "Self HP %",
        SkillConditionCheckResult.MULTIPLE_HP
    )
    self_buff_count = SkillConditionCategoryTargetInt(
        {
            SkillCondition.SELF_BUFF_0: 0,
            SkillCondition.SELF_BUFF_10: 10,
            SkillCondition.SELF_BUFF_20: 20,
            SkillCondition.SELF_BUFF_25: 25,
            SkillCondition.SELF_BUFF_30: 30,
            SkillCondition.SELF_BUFF_35: 35,
            SkillCondition.SELF_BUFF_40: 40,
            SkillCondition.SELF_BUFF_45: 45,
            SkillCondition.SELF_BUFF_50: 50,
        },
        SkillConditionMaxCount.SINGLE,
        "Self buff count",
        SkillConditionCheckResult.MULTIPLE_BUFF
    )
    skill_bullet_hit = SkillConditionCategoryTargetInt(
        {
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
        },
        SkillConditionMaxCount.SINGLE,
        "Skill bullet hit count",
        SkillConditionCheckResult.MULTIPLE_BULLET_HIT
    )
    skill_teammates_covered = SkillConditionCategoryTargetInt(
        {
            SkillCondition.COVER_TEAMMATE_0: 0,
            SkillCondition.COVER_TEAMMATE_1: 1,
            SkillCondition.COVER_TEAMMATE_2: 2,
            SkillCondition.COVER_TEAMMATE_3: 3,
        },
        SkillConditionMaxCount.SINGLE,
        "Skill effect teammates covered",
        SkillConditionCheckResult.MULTIPLE_TEAMMATE_COVERAGE
    )

    @classmethod
    def get_all_categories(cls) -> list[SkillConditionCategory]:
        """Get all skill condition categories."""
        return [val for name, val in vars(cls).items()
                if not callable(getattr(cls, name)) and not name.startswith("__")]
