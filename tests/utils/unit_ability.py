"""Implementations for checking the affliction effects."""
from dataclasses import dataclass
from typing import Any, Optional

from dlparse.enums import BuffParameter, ConditionComposite
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

    def __hash__(self):
        # x 1E5 for error tolerance
        return hash((self.condition_comp, self.parameter, int(self.rate * 1E5)))

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unable to compare {type(self.__class__)} with {type(other)}")

        return ((self.source_ability_id, int(self.parameter.value), self.rate)
                < (other.source_ability_id, int(other.parameter.value), other.rate))


def check_ability_effect_unit_match(
        actual_units: set[AbilityVariantEffectUnit], expected_info: set[AbilityEffectInfo], /,
        message: Any = None
):
    """Check if the info of the affliction units match."""
    has_probability = any(info.probability for info in expected_info)
    has_cooldown = any(info.cooldown_sec for info in expected_info)
    has_max_max_occurrences = any(info.max_occurrences for info in expected_info)

    actual_info = [
        AbilityEffectInfo(
            unit.source_ability_id, unit.condition_comp, unit.parameter, unit.rate,
            unit.probability_pct if has_probability else None,
            unit.cooldown_sec if has_cooldown else None,
            unit.max_occurrences if has_max_max_occurrences else None,
        )
        for unit in actual_units
    ]

    check_info_list_match(actual_info, expected_info, message=message)
