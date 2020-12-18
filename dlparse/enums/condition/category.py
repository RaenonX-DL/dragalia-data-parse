"""Classes for condition categories."""
from enum import Enum, auto
from typing import Any, Generic, Iterable, Optional, TypeVar, Union

from dlparse.errors import EnumConversionError
from .items import Condition
from ..ability_condition import AbilityCondition
from ..condition_base import ConditionCheckResultMixin
from ..element import Element
from ..status import Status

__all__ = ("ConditionCheckResult", "ConditionCategories", "ConditionMaxCount")


class ConditionCheckResult(ConditionCheckResultMixin, Enum):
    """Condition validating result."""

    PASS = auto()

    MULTIPLE_TARGET_ELEMENT = auto()
    MULTIPLE_HP_CONDITION = auto()
    MULTIPLE_HP_STATUS = auto()
    MULTIPLE_COMBO_COUNT = auto()
    MULTIPLE_BUFF_COUNT = auto()
    MULTIPLE_BUFF_ZONE_SELF = auto()
    MULTIPLE_BUFF_ZONE_ALLY = auto()
    MULTIPLE_BULLET_HIT = auto()
    MULTIPLE_TEAMMATE_COVERAGE = auto()
    MULTIPLE_BULLETS_ON_MAP = auto()
    MULTIPLE_ADDL_INPUTS = auto()
    MULTIPLE_ACTION_CANCEL = auto()
    MULTIPLE_ACTION_CONDITION = auto()
    MULTIPLE_GAUGE_FILLED = auto()
    MULTIPLE_LAPIS_CARD = auto()
    MULTIPLE_MISC = auto()

    INTERNAL_NOT_AFFLICTION_ONLY = auto()
    INTERNAL_NOT_TARGET_ELEMENTAL = auto()
    INTERNAL_NOT_HP_STATUS = auto()
    INTERNAL_NOT_HP_CONDITION = auto()
    INTERNAL_NOT_COMBO_COUNT = auto()
    INTERNAL_NOT_BUFF_COUNT = auto()
    INTERNAL_NOT_BUFF_ZONE_SELF = auto()
    INTERNAL_NOT_BUFF_ZONE_ALLY = auto()
    INTERNAL_NOT_BULLET_HIT_COUNT = auto()
    INTERNAL_NOT_TEAMMATE_COVERAGE = auto()
    INTERNAL_NOT_BULLETS_ON_MAP = auto()
    INTERNAL_NOT_ADDL_INPUTS = auto()
    INTERNAL_NOT_ACTION_CANCEL = auto()
    INTERNAL_NOT_ACTION_CONDITION = auto()
    INTERNAL_NOT_GAUGE_FILLED = auto()
    INTERNAL_NOT_LAPIS_CARD = auto()

    HAS_CONDITIONS_LEFT = auto()

    UNEXPECTED = auto()

    @classmethod
    def passing_enums(cls) -> set["ConditionCheckResult"]:
        return {cls.PASS}


class ConditionMaxCount(Enum):
    """Maximum count of conditions of a category allowed in a condition composite."""

    SINGLE = auto()
    MULTIPLE = auto()


T = TypeVar("T")


class ConditionCategory(Generic[T]):
    """A condition category."""

    RAISE_ERROR = object()  # Dummy object for conversion on missing

    def __init__(self, data: dict[Condition, T], max_count: ConditionMaxCount, name: str,
                 result_on_invalid: ConditionCheckResult):
        self._members = data
        self._max_count = max_count
        self._name = name
        self._result_on_invalid = result_on_invalid

    def __contains__(self, item):
        if not isinstance(item, Condition):
            return False

        return item in self.members

    def __repr__(self):
        return f"<ConditionCategory - {self._name}>"

    @property
    def name(self) -> str:
        """Get the name of the condition category."""
        return self._name

    @property
    def members(self) -> set[Condition]:
        """Get all members of this category."""
        return set(self._members.keys())

    @property
    def targets(self) -> set[T]:
        """Get all targets of this category."""
        return set(self._members.values())

    @property
    def conversion_dict(self) -> dict[Condition, T]:
        """Get the dict for the conversion, which the key is :class:`Condition` and the value is its target."""
        return self._members

    @property
    def max_count_allowed(self) -> ConditionMaxCount:
        """Get the maximum count of the condition allowed in a single condition composite."""
        return self._max_count

    @property
    def result_on_invalid(self) -> ConditionCheckResult:
        """Get the :class:`ConditionCheckResult` to return if the validation failed."""
        return self._result_on_invalid

    def convert(self, item: Condition, /, on_missing: Any = RAISE_ERROR) -> T:
        """
        Convert ``item`` to :class:`T`.

        ``on_missing`` will be returned if unconvertible.
        If this is not given or specified as ``RAISE_ERROR`` (default) and ``item`` in unconvertible,
        :class:`EnumConversionError` will be raised.

        :raises EnumConversionError: if `item` is unconvertible is `on_missing` is `RAISE_ERROR`
        """
        if item not in self:
            if on_missing is self.RAISE_ERROR:
                raise EnumConversionError(item, Condition, self._name)

            return on_missing

        return self._members[item]

    def convert_reversed(self, item: T) -> Condition:
        """
        Convert ``item`` from :class:`T` to :class:`Condition`.

        :raises EnumConversionError: if `item` is unconvertible
        """
        for condition, target in self._members.items():
            if item == target:
                return condition

        raise EnumConversionError(item, item.__class__, self._name)

    def extract(self, conditions: Iterable[Condition]) -> Union[set[Condition], Condition]:
        """
        Extract :class:`Condition` that belongs to this category from ``conditions``.

        Note that this does **NOT** validate ``conditions``, which means that if there are multiple conditions of
        this category exist in ``conditions`` while the maximum allowed count is set to
        ``ConditionMaxCount.SINGLE``, **NO** errors will be yielded.

        Instead, this will return the first element discovered. To validate ``conditions``,
        call ``is_valid()`` instead.
        """
        if self.max_count_allowed == ConditionMaxCount.SINGLE:
            return next((condition for condition in conditions if condition in self), None)

        return {condition for condition in conditions if condition in self}

    def is_valid(self, conditions: Iterable[Condition]) -> bool:
        """Check if ``conditions`` is valid."""
        if self.max_count_allowed == ConditionMaxCount.SINGLE:
            return len(set(conditions) & set(self.members)) <= 1

        return True


class ConditionCategoryTargetNumber(ConditionCategory[float]):
    """A condition category which target is :class:`float`."""

    def get_members_lte(self, threshold: float) -> list[Condition]:
        """Get the members which target is less than or equal to ``threshold``."""
        return [cond_enum for cond_enum, target in self._members.items() if target <= threshold]


class ConditionCategories:
    """Categories for various conditions (:class:`Condition`)."""

    # region 1xx - Target
    target_status = ConditionCategory[Status](
        {
            # Abnormal statuses
            Condition.TARGET_POISONED: Status.POISON,
            Condition.TARGET_BURNED: Status.BURN,
            Condition.TARGET_FROZEN: Status.FREEZE,
            Condition.TARGET_PARALYZED: Status.PARALYZE,
            Condition.TARGET_BLINDED: Status.BLIND,
            Condition.TARGET_STUNNED: Status.STUN,
            Condition.TARGET_CURSED: Status.CURSE,
            Condition.TARGET_BOGGED: Status.BOG,
            Condition.TARGET_SLEPT: Status.SLEEP,
            Condition.TARGET_FROSTBITTEN: Status.FROSTBITE,
            Condition.TARGET_FLASHBURNED: Status.FLASHBURN,
            Condition.TARGET_STORMLASHED: Status.STORMLASH,
            Condition.TARGET_SHADOWBLIGHTED: Status.SHADOWBLIGHT,
            # Special abnormal status
            Condition.TARGET_AFFLICTED: Status.AFFLICTED,
            Condition.TARGET_DEF_DOWN: Status.DEF_DOWNED,
            Condition.TARGET_BUFFED: Status.BUFFED,
            Condition.TARGET_DEBUFFED: Status.DEBUFFED,
            # Enemy state
            Condition.TARGET_BK_STATE: Status.BK_STATE
        },
        ConditionMaxCount.MULTIPLE,
        "Target - status",
        ConditionCheckResult.UNEXPECTED  # Impossible to fail (current only invalid reason is multiple conditions)
    )
    target_element = ConditionCategory[Element](
        {
            Condition.TARGET_ELEM_FLAME: Element.FLAME,
            Condition.TARGET_ELEM_WATER: Element.WATER,
            Condition.TARGET_ELEM_WIND: Element.WIND,
            Condition.TARGET_ELEM_LIGHT: Element.LIGHT,
            Condition.TARGET_ELEM_SHADOW: Element.SHADOW,
        },
        ConditionMaxCount.SINGLE,
        "Target - element",
        ConditionCheckResult.MULTIPLE_TARGET_ELEMENT
    )
    # endregion

    # region 2xx - Self status (general)
    self_hp_status = ConditionCategoryTargetNumber(
        {
            Condition.SELF_HP_1: 0,
            Condition.SELF_HP_EQ_10: 0.1,
            Condition.SELF_HP_EQ_20: 0.2,
            Condition.SELF_HP_EQ_30: 0.3,
            Condition.SELF_HP_EQ_50: 0.5,
            Condition.SELF_HP_EQ_70: 0.7,
            Condition.SELF_HP_FULL: 1,
        },
        ConditionMaxCount.SINGLE,
        "Self - HP status (of % max)",
        ConditionCheckResult.MULTIPLE_HP_STATUS
    )
    self_hp_cond = ConditionCategoryTargetNumber(
        {
            Condition.SELF_HP_LT_30: 0.3,
            Condition.SELF_HP_LT_40: 0.4,
            Condition.SELF_HP_GT_30: 0.3,
            Condition.SELF_HP_GTE_40: 0.4,
            Condition.SELF_HP_GTE_50: 0.5,
            Condition.SELF_HP_GTE_60: 0.6,
            Condition.SELF_HP_GTE_85: 0.85,
        },
        ConditionMaxCount.SINGLE,
        "Self - HP condition (of % max)",
        ConditionCheckResult.MULTIPLE_HP_CONDITION
    )
    self_combo_count = ConditionCategoryTargetNumber(
        {
            Condition.COMBO_0: 0,
            Condition.COMBO_5: 5,
            Condition.COMBO_10: 10,
            Condition.COMBO_15: 15,
            Condition.COMBO_20: 20,
            Condition.COMBO_25: 25,
            Condition.COMBO_30: 30,
        },
        ConditionMaxCount.SINGLE,
        "Self - combo count",
        ConditionCheckResult.MULTIPLE_COMBO_COUNT
    )
    self_buff_count = ConditionCategoryTargetNumber(
        {
            Condition.SELF_BUFF_0: 0,
            Condition.SELF_BUFF_1: 1,
            Condition.SELF_BUFF_2: 2,
            Condition.SELF_BUFF_3: 3,
            Condition.SELF_BUFF_4: 4,
            Condition.SELF_BUFF_5: 5,
            Condition.SELF_BUFF_6: 6,
            Condition.SELF_BUFF_7: 7,
            Condition.SELF_BUFF_8: 8,
            Condition.SELF_BUFF_9: 9,
            Condition.SELF_BUFF_10: 10,
            Condition.SELF_BUFF_15: 15,
            Condition.SELF_BUFF_20: 20,
            Condition.SELF_BUFF_25: 25,
            Condition.SELF_BUFF_30: 30,
            Condition.SELF_BUFF_35: 35,
            Condition.SELF_BUFF_40: 40,
            Condition.SELF_BUFF_45: 45,
            Condition.SELF_BUFF_50: 50,
        },
        ConditionMaxCount.SINGLE,
        "Self - buff count",
        ConditionCheckResult.MULTIPLE_BUFF_COUNT
    )
    self_in_buff_zone_self = ConditionCategoryTargetNumber(
        {
            Condition.SELF_IN_BUFF_ZONE_BY_SELF_0: 0,
            Condition.SELF_IN_BUFF_ZONE_BY_SELF_1: 1,
            Condition.SELF_IN_BUFF_ZONE_BY_SELF_2: 2,
        },
        ConditionMaxCount.SINGLE,
        "Self - count of self-built buff zones inside",
        ConditionCheckResult.MULTIPLE_BUFF_ZONE_SELF
    )
    self_in_buff_zone_ally = ConditionCategoryTargetNumber(
        {
            Condition.SELF_IN_BUFF_ZONE_BY_ALLY_0: 0,
            Condition.SELF_IN_BUFF_ZONE_BY_ALLY_1: 1,
            Condition.SELF_IN_BUFF_ZONE_BY_ALLY_2: 2,
            Condition.SELF_IN_BUFF_ZONE_BY_ALLY_3: 3,
        },
        ConditionMaxCount.SINGLE,
        "Self - count of ally-built buff zones inside",
        ConditionCheckResult.MULTIPLE_BUFF_ZONE_ALLY
    )
    # endregion

    # region 3xx - Skill animation/effect
    skill_bullet_hit = ConditionCategoryTargetNumber(
        {
            Condition.BULLET_HIT_1: 1,
            Condition.BULLET_HIT_2: 2,
            Condition.BULLET_HIT_3: 3,
            Condition.BULLET_HIT_4: 4,
            Condition.BULLET_HIT_5: 5,
            Condition.BULLET_HIT_6: 6,
            Condition.BULLET_HIT_7: 7,
            Condition.BULLET_HIT_8: 8,
            Condition.BULLET_HIT_9: 9,
            Condition.BULLET_HIT_10: 10,
        },
        ConditionMaxCount.SINGLE,
        "Skill - bullet hit count",
        ConditionCheckResult.MULTIPLE_BULLET_HIT
    )
    skill_teammates_covered = ConditionCategoryTargetNumber(
        {
            Condition.COVER_TEAMMATE_0: 0,
            Condition.COVER_TEAMMATE_1: 1,
            Condition.COVER_TEAMMATE_2: 2,
            Condition.COVER_TEAMMATE_3: 3,
        },
        ConditionMaxCount.SINGLE,
        "Skill - teammates covered by effect",
        ConditionCheckResult.MULTIPLE_TEAMMATE_COVERAGE
    )
    skill_bullets_on_map = ConditionCategoryTargetNumber(
        {
            Condition.BULLETS_ON_MAP_0: 0,
            Condition.BULLETS_ON_MAP_1: 1,
            Condition.BULLETS_ON_MAP_2: 2,
            Condition.BULLETS_ON_MAP_3: 3,
            Condition.BULLETS_ON_MAP_4: 4,
            Condition.BULLETS_ON_MAP_5: 5,
            Condition.BULLETS_ON_MAP_6: 6,
            Condition.BULLETS_ON_MAP_7: 7,
            Condition.BULLETS_ON_MAP_8: 8,
            Condition.BULLETS_ON_MAP_9: 9,
        },
        ConditionMaxCount.SINGLE,
        "Skill - bullets on map",
        ConditionCheckResult.MULTIPLE_BULLETS_ON_MAP
    )
    skill_addl_inputs = ConditionCategoryTargetNumber(
        {
            Condition.ADDL_INPUT_0: 0,
            Condition.ADDL_INPUT_1: 1,
            Condition.ADDL_INPUT_2: 2,
            Condition.ADDL_INPUT_3: 3,
            Condition.ADDL_INPUT_4: 4,
            Condition.ADDL_INPUT_5: 5,
            Condition.ADDL_INPUT_6: 6,
        },
        ConditionMaxCount.SINGLE,
        "Skill - additional input",
        ConditionCheckResult.MULTIPLE_ADDL_INPUTS
    )
    skill_action_cancel = ConditionCategoryTargetNumber(
        {
            Condition.CANCELS_FJOACHIM_S2: 991070,
        },
        ConditionMaxCount.SINGLE,
        "Skill - action cancel",
        ConditionCheckResult.MULTIPLE_ACTION_CANCEL
    )
    # endregion

    # region 4xx - Self status (special)
    action_condition = ConditionCategoryTargetNumber(
        {
            # Value is the corresponding Action Condition ID (not necessary means that it needs to exist)
            Condition.SELF_SIGIL_LOCKED: 1152,
            Condition.SELF_SIGIL_RELEASED: 1152,
            Condition.SELF_LAPIS_CARD_0: 1319,
            Condition.SELF_LAPIS_CARD_1: 1319,
            Condition.SELF_LAPIS_CARD_2: 1319,
            Condition.SELF_LAPIS_CARD_3: 1319,
        },
        ConditionMaxCount.SINGLE,
        "Self - action condition status",
        ConditionCheckResult.MULTIPLE_ACTION_CONDITION
    )
    self_gauge_filled = ConditionCategoryTargetNumber(
        {
            Condition.SELF_GAUGE_FILLED_0: 0,
            Condition.SELF_GAUGE_FILLED_1: 1,
            Condition.SELF_GAUGE_FILLED_2: 2,
        },
        ConditionMaxCount.SINGLE,
        "Self - gauge status",
        ConditionCheckResult.MULTIPLE_GAUGE_FILLED
    )
    self_lapis_card = ConditionCategoryTargetNumber(
        {
            Condition.SELF_LAPIS_CARD_0: 0,
            Condition.SELF_LAPIS_CARD_1: 1,
            Condition.SELF_LAPIS_CARD_2: 2,
            Condition.SELF_LAPIS_CARD_3: 3,
        },
        ConditionMaxCount.SINGLE,
        "Self - gauge status",
        ConditionCheckResult.MULTIPLE_LAPIS_CARD
    )
    # endregion

    # region 9xx - Miscellaneous
    misc = ConditionCategory[AbilityCondition](
        {
            Condition.QUEST_START: AbilityCondition.QUEST_START,
        },
        ConditionMaxCount.SINGLE,
        "Miscellaneous",
        ConditionCheckResult.MULTIPLE_MISC
    )
    # endregion

    _action_cond_cat: dict[int, ConditionCategory] = {
        1319: self_lapis_card
    }

    @classmethod
    def get_all_categories(cls) -> list[ConditionCategory]:
        """Get all condition categories."""
        return [
            val for name, val in vars(cls).items()
            if not callable(getattr(cls, name)) and not name.startswith("_")
        ]

    @classmethod
    def get_category_action_condition(cls, action_cond_id: int) -> Optional[ConditionCategory]:
        """
        Get the condition category corresponds to the action condition.

        Return ``None`` if no corresponding condition category.
        """
        return cls._action_cond_cat.get(action_cond_id)
