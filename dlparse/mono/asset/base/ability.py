"""Common classes for the ability data."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

from dlparse.enums import (
    AbilityCondition, AbilityTargetAction, AbilityVariantType, Condition, ConditionCategories, SkillNumber, Status,
)
from dlparse.errors import EnumConversionError
from .master import MasterEntryBase

__all__ = ("AbilityConditionEntryBase", "AbilityVariantEntryBase", "AbilityEntryBase")

_ability_condition_map: dict[AbilityCondition, Condition] = {
    AbilityCondition.NONE: Condition.NONE,
    AbilityCondition.TRG_SELF_HP_LTE: Condition.ON_SELF_HP_LTE_30,
    AbilityCondition.TRG_RECEIVED_BUFF_DEF: Condition.ON_SELF_BUFFED_DEF,
    AbilityCondition.TRG_QUEST_START: Condition.QUEST_START,
    AbilityCondition.TRG_ENERGIZED: Condition.SELF_ENERGIZED,
    AbilityCondition.TRG_SHAPESHIFT_COMPLETED: Condition.SELF_SHAPESHIFT_COMPLETED,
}
"""
A dict that maps :class:`AbilityCondition` to :class:`Condition`.

This only contains :class:`AbilityCondition` that do not require additional parameter checks.
Missing key in this map does not mean that it is not handled.
"""

_hp_gte_map: dict[float, Condition] = {
    30: Condition.SELF_HP_GTE_30,
    40: Condition.SELF_HP_GTE_40,
    50: Condition.SELF_HP_GTE_50,
    60: Condition.SELF_HP_GTE_60,
    70: Condition.SELF_HP_GTE_70,
    85: Condition.SELF_HP_GTE_85,
    100: Condition.SELF_HP_FULL,
}
"""A dict that maps a certain HP threshold percentage to a :class:`Condition`."""


@dataclass
class AbilityConditionEntryBase(ABC):
    """Base class of an ability condition entry."""

    condition_code: int

    val_1: float

    probability: float

    condition_type: AbilityCondition = field(init=False)

    def __post_init__(self):
        self.condition_type = AbilityCondition(self.condition_code)

    @abstractmethod
    def _condition_unconvertible(self, ex: Optional[Exception] = None):
        """Method to call if the condition is unconvertible."""
        raise NotImplementedError()

    def _cond_self_buffed_additional(self) -> Optional[Condition]:
        """
        Additional method to call when calling ``self._cond_self_buffed``.

        Return ``None`` if none of the conditions match in this method.
        Otherwise, return the corresponding condition.
        """
        # pylint: disable=no-self-use
        # This method is intended to leave with ``self``
        # because the implementation that overrides this method may need to use that ``self``.
        return None

    def _cond_self_buffed(self) -> Condition:
        if condition := self._cond_self_buffed_additional():
            return condition

        if self.val_1 == 1380:
            return Condition.SELF_GLEONIDAS_FULL_STACKS

        raise self._condition_unconvertible()

    def _cond_self_hp(self) -> Optional[Condition]:
        # Self HP >=
        if self.condition_type in (AbilityCondition.EFF_SELF_HP_GTE, AbilityCondition.EFF_SELF_HP_GTE_2):
            return self._cond_self_hp_gte()

        # Self HP <
        if self.condition_type in (AbilityCondition.EFF_SELF_HP_LT, AbilityCondition.EFF_SELF_HP_LT_2):
            return self._cond_self_hp_lt()

        return None

    def _cond_self_hp_gte(self) -> Condition:
        if condition := _hp_gte_map.get(self.val_1):
            return condition

        raise self._condition_unconvertible()

    def _cond_self_hp_lt(self) -> Condition:
        if self.val_1 == 30:
            return Condition.SELF_HP_LT_30
        if self.val_1 == 40:
            return Condition.SELF_HP_LT_40

        raise self._condition_unconvertible()

    def _cond_self_in_dragon(self) -> Condition:
        if self.val_1 == 0 or self.val_1 == 1:
            return Condition.SELF_SHAPESHIFTED_1_TIME_IN_DRAGON
        if self.val_1 == 2:
            return Condition.SELF_SHAPESHIFTED_2_TIMES_IN_DRAGON

        raise self._condition_unconvertible()

    def _cond_hit_by_affliction(self) -> Condition:
        try:
            return ConditionCategories.trigger_hit_by_affliction.convert_reversed(Status(self.val_1))
        except EnumConversionError as ex:
            raise self._condition_unconvertible(ex)

    def to_condition(self) -> Condition:
        """
        Convert the ability condition to condition.

        :raises AbilityConditionUnconvertibleError: if the ability condition is unconvertible
        """
        ability_condition = _ability_condition_map.get(self.condition_type)
        if ability_condition is not None:  # Explicit check because ``Condition.NONE`` is falsy
            return ability_condition

        # Self in-dragon
        if self.condition_type == AbilityCondition.EFF_IS_DRAGON:
            return self._cond_self_in_dragon()

        # Self HP condition
        if self_hp_cond := self._cond_self_hp():
            return self_hp_cond

        # Hit by attack with affliction
        if self.condition_type == AbilityCondition.TRG_HIT_WITH_AFFLICTION:
            return self._cond_hit_by_affliction()

        # Has specific buff
        if self.condition_type == AbilityCondition.EFF_SELF_SPECIFICALLY_BUFFED:
            return self._cond_self_buffed()

        raise self._condition_unconvertible()

    @property
    def is_unknown_condition(self) -> bool:
        """Check if the condition type is unknown."""
        return self.condition_type == AbilityCondition.UNKNOWN


@dataclass
class AbilityVariantEntryBase(ABC):
    """Base class of an ability variant entry."""

    type_id: int
    id_a: int
    target_action_id: int
    up_value: float

    type_enum: AbilityVariantType = field(init=False)
    target_action_enum: AbilityTargetAction = field(init=False)

    def __post_init__(self):
        self.type_enum = AbilityVariantType(self.type_id)
        self.target_action_enum = AbilityTargetAction(self.target_action_id)

    @property
    def is_not_used(self) -> bool:
        """Check if the variant is not used."""
        return self.type_enum == AbilityVariantType.NOT_USED

    @property
    def is_unknown_type(self):
        """Check if the variant type is unknown."""
        return self.type_enum == AbilityVariantType.UNKNOWN

    @property
    def is_boosted_by_combo(self) -> bool:
        """Check if the variant type is to boost the damage according to the combo count."""
        return self.type_enum == AbilityVariantType.DMG_UP_ON_COMBO

    @property
    def is_boosted_by_gauge_status(self) -> bool:
        """Check if the damage will be boosted according to the gauge status."""
        return self.type_enum == AbilityVariantType.GAUGE_STATUS

    @property
    def assigned_action_condition(self) -> Optional[int]:
        """Get the assigned action condition ID. Return ``None`` if unavailable."""
        return self.id_a if self.type_enum == AbilityVariantType.CHANGE_STATE else None

    @property
    def other_ability_id(self) -> Optional[int]:
        """Get the other ability ID assigned. Return ``None`` if unavailable."""
        return self.id_a if self.type_enum == AbilityVariantType.OTHER_ABILITY else None

    @property
    def enhanced_skill(self) -> Optional[tuple[int, SkillNumber]]:
        """Get the enhanced skill ID and its skill number. Return ``None`` if unavailable."""
        return (
            (self.id_a, self.target_action_enum.to_skill_num)
            if self.type_enum == AbilityVariantType.ENHANCE_SKILL else None
        )


C = TypeVar("C", bound=AbilityConditionEntryBase)  # pylint: disable=invalid-name
V = TypeVar("V", bound=AbilityVariantEntryBase)  # pylint: disable=invalid-name


@dataclass
class AbilityEntryBase(Generic[C, V], MasterEntryBase, ABC):
    """Base class of an ability entry."""

    condition: C

    @property
    @abstractmethod
    def variants(self) -> list[V]:
        """
        Get all in-use ability variants as a list.

        Note that this does **not** give the other variants that come from different ability linked by the variants.
        To get all possible variants, call ``get_variants()`` instead.
        """
        raise NotImplementedError()

    @property
    def unknown_variant_type_ids(self) -> list[int]:
        """Get a list of unknown variant type IDs."""
        return [variant.type_id for variant in self.variants if variant.is_unknown_type]
