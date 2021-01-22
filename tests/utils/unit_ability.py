"""Implementations for checking the affliction effects."""
from dataclasses import dataclass
from typing import Any, Optional

from dlparse.enums import AbilityTargetAction, BuffParameter, ConditionComposite, HitTargetSimple
from dlparse.model import AbilityVariantEffectUnit
from .unit_base import AbilityInfoBase, check_info_list_match

__all__ = ("AbilityEffectInfo", "check_ability_effect_unit_match")


@dataclass
class AbilityEffectInfo(AbilityInfoBase):
    """A single affliction info entry."""

    condition_comp: ConditionComposite
    parameter: BuffParameter
    rate: float
    probability: Optional[float] = None
    cooldown_sec: Optional[float] = None
    max_occurrences: Optional[int] = None
    target: Optional[HitTargetSimple] = None
    target_action: Optional[AbilityTargetAction] = None
    duration_time: Optional[float] = None

    def __hash__(self):
        # x 1E5 for error tolerance
        return hash((self.condition_comp.conditions_sorted, self.parameter, int(self.rate * 1E5)))

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unable to compare {type(self.__class__)} with {type(other)}")

        data_self = (
            self.source_ability_id,
            self.condition_comp.conditions_sorted,
            int(self.parameter.value),
            self.rate
        )

        data_other = (
            other.source_ability_id,
            other.condition_comp.conditions_sorted,
            int(other.parameter.value),
            other.rate
        )

        return data_self < data_other


def check_ability_effect_unit_match(
        actual_units: set[AbilityVariantEffectUnit], expected_info: set[AbilityEffectInfo], /,
        message: Any = None
):
    """Check if the info of the affliction units match."""
    has_probability = any(info.probability for info in expected_info)
    has_cooldown = any(info.cooldown_sec for info in expected_info)
    has_max_occurrences = any(info.max_occurrences for info in expected_info)
    has_target = any(info.target for info in expected_info)
    has_target_action = any(info.target_action for info in expected_info)
    has_duration = any(info.duration_time for info in expected_info)

    actual_info = [
        AbilityEffectInfo(
            source_ability_id=unit.source_ability_id,
            condition_comp=unit.condition_comp,
            parameter=unit.parameter, rate=unit.rate,
            probability=unit.probability_pct if has_probability else None,
            cooldown_sec=unit.cooldown_sec if has_cooldown else None,
            max_occurrences=unit.max_occurrences if has_max_occurrences else None,
            target=unit.target if has_target else None,
            target_action=unit.target_action if has_target_action else None,
            duration_time=unit.duration_time if has_duration else None,
        )
        for unit in actual_units
    ]

    check_info_list_match(actual_info, expected_info, message=message)
