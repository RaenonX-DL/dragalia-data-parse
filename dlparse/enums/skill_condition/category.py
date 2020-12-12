"""Classes for skill condition categories."""
from enum import Enum, auto
from typing import Any, Generic, Iterable, TypeVar, Union

from dlparse.errors import EnumConversionError
from .items import SkillCondition
from ..condition_base import ConditionCheckResultMixin
from ..element import Element
from ..status import Status

__all__ = ("SkillConditionCheckResult", "SkillConditionCategories", "SkillConditionMaxCount")


class SkillConditionCheckResult(ConditionCheckResultMixin, Enum):
    """Skill conditions validating result."""

    PASS = auto()

    MULTIPLE_TARGET_ELEMENT = auto()
    MULTIPLE_HP_CONDITION = auto()
    MULTIPLE_HP_STATUS = auto()
    MULTIPLE_COMBO_COUNT = auto()
    MULTIPLE_BUFF_COUNT = auto()
    MULTIPLE_BUFF_ZONE_SELF = auto()
    MULTIPLE_BUFF_ZONE_ALLY = auto()
    MULTIPLE_SELF_ACTION_CONDITION = auto()
    MULTIPLE_GAUGE_FILLED = auto()
    MULTIPLE_BULLET_HIT = auto()
    MULTIPLE_TEAMMATE_COVERAGE = auto()
    MULTIPLE_BULLETS_ON_MAP = auto()
    MULTIPLE_ADDL_INPUTS = auto()
    MULTIPLE_ACTION_CANCEL = auto()

    INTERNAL_NOT_AFFLICTION_ONLY = auto()
    INTERNAL_NOT_TARGET_ELEMENTAL = auto()
    INTERNAL_NOT_HP_STATUS = auto()
    INTERNAL_NOT_HP_CONDITION = auto()
    INTERNAL_NOT_COMBO_COUNT = auto()
    INTERNAL_NOT_BUFF_COUNT = auto()
    INTERNAL_NOT_BUFF_ZONE_SELF = auto()
    INTERNAL_NOT_BUFF_ZONE_ALLY = auto()
    INTERNAL_NOT_SELF_ACTION_CONDITION = auto()
    INTERNAL_NOT_GAUGE_FILLED = auto()
    INTERNAL_NOT_BULLET_HIT_COUNT = auto()
    INTERNAL_NOT_TEAMMATE_COVERAGE = auto()
    INTERNAL_NOT_BULLETS_ON_MAP = auto()
    INTERNAL_NOT_ADDL_INPUTS = auto()
    INTERNAL_NOT_ACTION_CANCEL = auto()

    HAS_CONDITIONS_LEFT = auto()

    UNEXPECTED = auto()

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

    RAISE_ERROR = object()  # Dummy object for conversion on missing

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

    def convert(self, item: SkillCondition, /, on_missing: Any = RAISE_ERROR) -> T:
        """
        Convert ``item`` to :class:`T`.

        ``on_missing`` will be returned if unconvertible.
        If this is not given or specified as ``RAISE_ERROR`` (default) and ``item`` in unconvertible,
        :class:`EnumConversionError` will be raised.

        :raises EnumConversionError: if `item` is unconvertible is `on_missing` is `RAISE_ERROR`
        """
        if item not in self:
            if on_missing is self.RAISE_ERROR:
                raise EnumConversionError(item, SkillCondition, self._name)

            return on_missing

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


class SkillConditionCategoryTargetNumber(SkillConditionCategory[float]):
    """A skill condition category which target is :class:`float`."""

    def get_members_lte(self, threshold: float) -> list[SkillCondition]:
        """Get the members which target is less than or equal to ``threshold``."""
        return [cond_enum for cond_enum, target in self._members.items() if target <= threshold]


class SkillConditionCategories:
    """Categories for skill conditions (:class:`SkillCondition`)."""

    # pylint: disable=too-few-public-methods

    target_status = SkillConditionCategory[Status](
        {
            # Abnormal statuses
            SkillCondition.TARGET_POISONED: Status.POISON,
            SkillCondition.TARGET_BURNED: Status.BURN,
            SkillCondition.TARGET_FROZEN: Status.FREEZE,
            SkillCondition.TARGET_PARALYZED: Status.PARALYZE,
            SkillCondition.TARGET_BLINDED: Status.BLIND,
            SkillCondition.TARGET_STUNNED: Status.STUN,
            SkillCondition.TARGET_CURSED: Status.CURSE,
            SkillCondition.TARGET_BOGGED: Status.BOG,
            SkillCondition.TARGET_SLEPT: Status.SLEEP,
            SkillCondition.TARGET_FROSTBITTEN: Status.FROSTBITE,
            SkillCondition.TARGET_FLASHBURNED: Status.FLASHBURN,
            SkillCondition.TARGET_STORMLASHED: Status.STORMLASH,
            SkillCondition.TARGET_SHADOWBLIGHTED: Status.SHADOWBLIGHT,
            # Special abnormal status
            SkillCondition.TARGET_AFFLICTED: Status.AFFLICTED,
            SkillCondition.TARGET_DEF_DOWN: Status.DEF_DOWNED,
            SkillCondition.TARGET_BUFFED: Status.BUFFED,
            SkillCondition.TARGET_DEBUFFED: Status.DEBUFFED,
            # Enemy state
            SkillCondition.TARGET_BK_STATE: Status.BK_STATE
        },
        SkillConditionMaxCount.MULTIPLE,
        "Target - status",
        SkillConditionCheckResult.UNEXPECTED  # Impossible to fail (current only invalid reason is multiple conditions)
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
        "Target - element",
        SkillConditionCheckResult.MULTIPLE_TARGET_ELEMENT
    )
    self_hp_status = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.SELF_HP_1: 0,
            SkillCondition.SELF_HP_EQ_10: 0.1,
            SkillCondition.SELF_HP_EQ_20: 0.2,
            SkillCondition.SELF_HP_EQ_30: 0.3,
            SkillCondition.SELF_HP_EQ_50: 0.5,
            SkillCondition.SELF_HP_EQ_70: 0.7,
            SkillCondition.SELF_HP_FULL: 1,
        },
        SkillConditionMaxCount.SINGLE,
        "Self - HP status (of % max)",
        SkillConditionCheckResult.MULTIPLE_HP_STATUS
    )
    self_hp_cond = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.SELF_HP_LT_30: 0.3,
            SkillCondition.SELF_HP_LT_40: 0.4,
            SkillCondition.SELF_HP_GT_30: 0.3,
            SkillCondition.SELF_HP_GTE_40: 0.4,
            SkillCondition.SELF_HP_GTE_50: 0.5,
            SkillCondition.SELF_HP_GTE_60: 0.6,
            SkillCondition.SELF_HP_GTE_85: 0.85,
        },
        SkillConditionMaxCount.SINGLE,
        "Self - HP condition (of % max)",
        SkillConditionCheckResult.MULTIPLE_HP_CONDITION
    )
    self_combo_count = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.COMBO_0: 0,
            SkillCondition.COMBO_5: 5,
            SkillCondition.COMBO_10: 10,
            SkillCondition.COMBO_15: 15,
            SkillCondition.COMBO_20: 20,
            SkillCondition.COMBO_25: 25,
            SkillCondition.COMBO_30: 30,
        },
        SkillConditionMaxCount.SINGLE,
        "Self - combo count",
        SkillConditionCheckResult.MULTIPLE_COMBO_COUNT
    )
    self_buff_count = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.SELF_BUFF_0: 0,
            SkillCondition.SELF_BUFF_1: 1,
            SkillCondition.SELF_BUFF_2: 2,
            SkillCondition.SELF_BUFF_3: 3,
            SkillCondition.SELF_BUFF_4: 4,
            SkillCondition.SELF_BUFF_5: 5,
            SkillCondition.SELF_BUFF_6: 6,
            SkillCondition.SELF_BUFF_7: 7,
            SkillCondition.SELF_BUFF_8: 8,
            SkillCondition.SELF_BUFF_9: 9,
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
        "Self - buff count",
        SkillConditionCheckResult.MULTIPLE_BUFF_COUNT
    )
    self_in_buff_zone_self = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_0: 0,
            SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_1: 1,
            SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_2: 2,
        },
        SkillConditionMaxCount.SINGLE,
        "Self - count of self-built buff zones inside",
        SkillConditionCheckResult.MULTIPLE_BUFF_ZONE_SELF
    )
    self_in_buff_zone_ally = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_0: 0,
            SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_1: 1,
            SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_2: 2,
            SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_3: 3,
        },
        SkillConditionMaxCount.SINGLE,
        "Self - count of ally-built buff zones inside",
        SkillConditionCheckResult.MULTIPLE_BUFF_ZONE_ALLY
    )
    self_action_condition = SkillConditionCategoryTargetNumber(
        {
            # Value is the corresponding Action Condition ID (not necessary means that it needs to exist)
            SkillCondition.SELF_SIGIL_LOCKED: 1152,
            SkillCondition.SELF_SIGIL_RELEASED: 1152,
        },
        SkillConditionMaxCount.SINGLE,
        "Self - action condition status",
        SkillConditionCheckResult.MULTIPLE_SELF_ACTION_CONDITION
    )
    self_gauge_filled = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.SELF_GAUGE_FILLED_0: 0,
            SkillCondition.SELF_GAUGE_FILLED_1: 1,
            SkillCondition.SELF_GAUGE_FILLED_2: 2,
        },
        SkillConditionMaxCount.SINGLE,
        "Self - gauge status",
        SkillConditionCheckResult.MULTIPLE_GAUGE_FILLED
    )
    skill_bullet_hit = SkillConditionCategoryTargetNumber(
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
        "Skill - bullet hit count",
        SkillConditionCheckResult.MULTIPLE_BULLET_HIT
    )
    skill_teammates_covered = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.COVER_TEAMMATE_0: 0,
            SkillCondition.COVER_TEAMMATE_1: 1,
            SkillCondition.COVER_TEAMMATE_2: 2,
            SkillCondition.COVER_TEAMMATE_3: 3,
        },
        SkillConditionMaxCount.SINGLE,
        "Skill - teammates covered by effect",
        SkillConditionCheckResult.MULTIPLE_TEAMMATE_COVERAGE
    )
    skill_bullets_on_map = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.BULLETS_ON_MAP_0: 0,
            SkillCondition.BULLETS_ON_MAP_1: 1,
            SkillCondition.BULLETS_ON_MAP_2: 2,
            SkillCondition.BULLETS_ON_MAP_3: 3,
            SkillCondition.BULLETS_ON_MAP_4: 4,
            SkillCondition.BULLETS_ON_MAP_5: 5,
            SkillCondition.BULLETS_ON_MAP_6: 6,
            SkillCondition.BULLETS_ON_MAP_7: 7,
            SkillCondition.BULLETS_ON_MAP_8: 8,
            SkillCondition.BULLETS_ON_MAP_9: 9,
        },
        SkillConditionMaxCount.SINGLE,
        "Skill - bullets on map",
        SkillConditionCheckResult.MULTIPLE_BULLETS_ON_MAP
    )
    skill_addl_inputs = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.ADDL_INPUT_0: 0,
            SkillCondition.ADDL_INPUT_1: 1,
            SkillCondition.ADDL_INPUT_2: 2,
            SkillCondition.ADDL_INPUT_3: 3,
            SkillCondition.ADDL_INPUT_4: 4,
            SkillCondition.ADDL_INPUT_5: 5,
            SkillCondition.ADDL_INPUT_6: 6,
        },
        SkillConditionMaxCount.SINGLE,
        "Skill - additional input",
        SkillConditionCheckResult.MULTIPLE_ADDL_INPUTS
    )
    skill_action_cancel = SkillConditionCategoryTargetNumber(
        {
            SkillCondition.CANCELS_FJOACHIM_S2: 991070,
        },
        SkillConditionMaxCount.SINGLE,
        "Skill - action cancel",
        SkillConditionCheckResult.MULTIPLE_ACTION_CANCEL
    )

    @classmethod
    def get_all_categories(cls) -> list[SkillConditionCategory]:
        """Get all skill condition categories."""
        return [val for name, val in vars(cls).items()
                if not callable(getattr(cls, name)) and not name.startswith("__")]
