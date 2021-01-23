"""Common classes for the ability data."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Generic, Optional, TypeVar

from dlparse.enums import (
    AbilityCondition, AbilityTargetAction, AbilityVariantType, ActionDebuffType, Condition, ConditionCategories,
    ConditionComposite, Element, SkillNumber, Status, UnitType, Weapon,
)
from dlparse.errors import EnumConversionError
from .master import MasterEntryBase

__all__ = ("AbilityConditionEntryBase", "AbilityVariantEntryBase", "AbilityEntryBase")

_hp_gte_map: dict[float, Condition] = {
    30: Condition.SELF_HP_GTE_30,
    40: Condition.SELF_HP_GTE_40,
    50: Condition.SELF_HP_GTE_50,
    60: Condition.SELF_HP_GTE_60,
    70: Condition.SELF_HP_GTE_70,
    80: Condition.SELF_HP_GTE_80,
    85: Condition.SELF_HP_GTE_85,
    100: Condition.SELF_HP_FULL,
}
"""A dict that maps a certain HP threshold percentage to a :class:`Condition`."""


@dataclass
class AbilityConditionEntryBase(ABC):
    """Base class of an ability condition entry."""

    condition_code: int

    unit_type: UnitType
    elemental_restriction: Element
    weapon_restriction: Weapon

    val_1: float

    probability: float

    condition_type: AbilityCondition = field(init=False)

    _cond_map: dict[AbilityCondition, Condition] = field(init=False)
    _cond_method_map: dict[AbilityCondition, Callable[[], Condition]] = field(init=False)

    def __post_init__(self):
        self.condition_type = AbilityCondition(self.condition_code)

        self._cond_map: dict[AbilityCondition, Condition] = {
            AbilityCondition.NONE: Condition.NONE,
            AbilityCondition.EFF_TARGET_OVERDRIVE: Condition.TARGET_OD_STATE,
            # Directly returns ``Condition.ON_COMBO_RESET`` and disregard the value because
            # combo count "resets" instead of gradually decreasing
            AbilityCondition.TRG_COMBO_COUNT_LT: Condition.ON_COMBO_RESET,
            AbilityCondition.TRG_RECEIVED_BUFF_DEF: Condition.ON_BUFFED_DEF,
            AbilityCondition.TRG_QUEST_START: Condition.QUEST_START,
            AbilityCondition.TRG_ENERGY_LV_UP: Condition.ON_ENERGY_LV_UP,
            AbilityCondition.TRG_ENERGIZED: Condition.SELF_ENERGIZED,
            # Despite the ability condition seems to be effective instead of triggering,
            # mapping to a triggering condition (``ON_INTO_BUFF_ZONE``)
            # makes more sense (the effect is granted once the user gets into the buff zone) and
            # gives easier categorization (no need to mess with the sectioned conditions or to create a new category)
            AbilityCondition.EFF_IN_BUFF_ZONE: Condition.ON_ENTERED_BUFF_ZONE,
            AbilityCondition.TRG_SHAPESHIFT_COMPLETED: Condition.SELF_SHAPESHIFT_COMPLETED,
            AbilityCondition.TRG_GOT_HIT: Condition.ON_HIT,
        }
        self._cond_method_map = {
            AbilityCondition.EFF_IN_DRAGON: self._cond_self_in_dragon,
            AbilityCondition.TRG_COMBO_COUNT_GTE: self._cond_combo_count_gte,
            AbilityCondition.TRG_COMBO_COUNT_DIV: self._cond_combo_count_div,
            AbilityCondition.EFF_TARGET_DEBUFFED: self._cond_target_debuffed,
            AbilityCondition.EFF_TARGET_AFFLICTED: self._cond_target_afflicted,
            AbilityCondition.EFF_SELF_BUFFED_ACTION_COND: self._cond_self_buffed,
            AbilityCondition.TRG_GOT_HIT_WITH_AFFLICTION: self._cond_hit_by_affliction,
            AbilityCondition.TRG_INFLICTED_TARGET: self._cond_inflicted_target,
        }

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
        # Self HP >= (effect)
        if self.condition_type in (AbilityCondition.EFF_SELF_HP_GT, AbilityCondition.EFF_SELF_HP_GTE_2):
            return self._cond_self_hp_gte()

        # Self HP >= (trigger)
        if self.condition_type in (AbilityCondition.TRG_SELF_HP_GT, AbilityCondition.TRG_SELF_HP_GTE):
            return self._cond_self_hp_gte_trigger()

        # Self HP < (effect)
        if self.condition_type in (AbilityCondition.EFF_SELF_HP_LT, AbilityCondition.EFF_SELF_HP_LT_2):
            return self._cond_self_hp_lt()

        # Self HP < (trigger)
        trg_cond_hp_lt = (
            AbilityCondition.TRG_SELF_HP_LT,
            AbilityCondition.TRG_SELF_HP_LT_2,
            AbilityCondition.TRG_SELF_HP_LTE
        )
        if self.condition_type in trg_cond_hp_lt:
            return self._cond_self_hp_lt_trigger()

        return None

    def _cond_self_hp_gte(self) -> Condition:
        if condition := _hp_gte_map.get(self.val_1):
            return condition

        raise self._condition_unconvertible()

    def _cond_self_hp_gte_trigger(self) -> Condition:
        if self.val_1 == 40:
            return Condition.ON_SELF_HP_GTE_40
        if self.val_1 == 60:
            return Condition.ON_SELF_HP_GTE_60

        raise self._condition_unconvertible()

    def _cond_self_hp_lt(self) -> Condition:
        if self.val_1 == 30:
            return Condition.SELF_HP_LT_30
        if self.val_1 == 40:
            return Condition.SELF_HP_LT_40

        raise self._condition_unconvertible()

    def _cond_self_hp_lt_trigger(self) -> Condition:
        if self.val_1 == 30:
            return Condition.ON_SELF_HP_LT_30
        if self.val_1 == 40:
            return Condition.ON_SELF_HP_LT_40
        if self.val_1 == 60:
            return Condition.ON_SELF_HP_LT_60

        raise self._condition_unconvertible()

    def _cond_self_in_dragon(self) -> Condition:
        if self.val_1 == 0 or self.val_1 == 1:
            return Condition.SELF_SHAPESHIFTED_1_TIME_IN_DRAGON
        if self.val_1 == 2:
            return Condition.SELF_SHAPESHIFTED_2_TIMES_IN_DRAGON

        raise self._condition_unconvertible()

    def _cond_combo_count_gte(self) -> Condition:
        if self.val_1 == 10:
            return Condition.ON_COMBO_GTE_10

        raise self._condition_unconvertible()

    def _cond_combo_count_div(self) -> Condition:
        if self.val_1 == 20:
            return Condition.ON_COMBO_DIV_BY_20
        if self.val_1 == 50:
            return Condition.ON_COMBO_DIV_BY_50

        raise self._condition_unconvertible()

    def _cond_target_debuffed(self) -> Condition:
        debuff_type = ActionDebuffType(self.val_1)

        if debuff_type == ActionDebuffType.DEF_DOWN:
            return Condition.TARGET_DEF_DOWN

        if debuff_type == ActionDebuffType.ATK_OR_DEF_DOWN:
            return Condition.TARGET_ATK_OR_DEF_DOWN

        raise self._condition_unconvertible()

    def _cond_target_afflicted(self) -> Condition:
        return ConditionCategories.target_status.convert_reversed(Status(self.val_1))

    def _cond_inflicted_target(self) -> Condition:
        return ConditionCategories.target_status_infliction.convert_reversed(Status(self.val_1))

    def _cond_hit_by_affliction(self) -> Condition:
        try:
            return ConditionCategories.trigger_hit_by_affliction.convert_reversed(Status(self.val_1))
        except EnumConversionError as ex:
            raise self._condition_unconvertible(ex)

    def _from_elem_restriction(self) -> Optional[Condition]:
        if not self.elemental_restriction.is_valid:
            return None

        return ConditionCategories.target_element.convert_reversed(self.elemental_restriction)

    def _from_weapon_restriction(self) -> Optional[Condition]:
        if not self.weapon_restriction.is_valid:
            return None

        return ConditionCategories.self_weapon_type.convert_reversed(self.weapon_restriction)

    def to_condition_comp(self) -> ConditionComposite:
        """
        Convert this ability condition to a condition composite.

        :raises AbilityConditionUnconvertibleError: if the ability condition is unconvertible
        """
        base_conds: list[Condition] = []

        # Get condition from the condition type fields
        ability_condition = self._cond_map.get(self.condition_type)
        if ability_condition is not None:  # Explicit check because ``Condition.NONE`` is falsy
            # Direct single condition
            base_conds.append(ability_condition)
        elif cond_method := self._cond_method_map.get(self.condition_type):
            # Mapped condition
            base_conds.append(cond_method())
        elif self_hp_cond := self._cond_self_hp():
            # Self HP condition
            base_conds.append(self_hp_cond)

        # Raise error if no conditions are yielded (condition unrecognizable)
        # Note that "none" condition is returned from ``self._cond_map`` (direct single condition)
        if not base_conds:
            raise self._condition_unconvertible()

        # Get additional conditions from the elemental and weapon restriction
        if elem_cond := self._from_elem_restriction():
            base_conds.append(elem_cond)

        if weapon_cond := self._from_weapon_restriction():
            base_conds.append(weapon_cond)

        # Create a condition composite and return it
        return ConditionComposite(base_conds)

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


CT = TypeVar("CT", bound=AbilityConditionEntryBase)
VT = TypeVar("VT", bound=AbilityVariantEntryBase)


@dataclass
class AbilityEntryBase(Generic[CT, VT], MasterEntryBase, ABC):
    """Base class of an ability entry."""

    condition: CT

    @property
    @abstractmethod
    def variants(self) -> list[VT]:
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
