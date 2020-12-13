"""Implementations for checking the debuffing effects."""
from dataclasses import dataclass
from typing import Any

import pytest

from dlparse.enums import BuffParameter
from dlparse.model import ActionConditionEffectUnit
from .unit_base import BuffInfoBase, check_info_list_match

__all__ = ("DebuffInfo", "check_debuff_unit_match")


@dataclass
class DebuffInfo(BuffInfoBase):
    """A single debuff info entry."""

    parameter: BuffParameter
    rate: float

    probability_pct: float  # 90 = 90%
    duration: float

    stackable: bool

    def __hash__(self):
        return hash((self.parameter, self.rate, self.probability_pct, self.duration, self.stackable, self.hit_label))


def check_debuff_unit_match(
        actual_units: list[ActionConditionEffectUnit], expected_info: list[DebuffInfo], /,
        message: Any = None
):
    """
    Check if the info of the debuff units match.

    This additionally checks if the rate is < 0 (debuff).
    """
    # Check for non-sense (>= 0) rate
    for actual_unit, expected_info_single in zip(actual_units, expected_info):
        if actual_unit.rate > 0:
            pytest.fail(f"A unit in the actual return has a rate of {actual_unit.rate} which is > 0. "
                        f"Debuffs should have either a rate of 0 (for example, mark) or < 0 (for example, DEF down)"
                        f"\n{actual_unit}")

        if expected_info_single.rate > 0:
            pytest.fail(f"A unit in the expected return has a rate of {expected_info_single.rate} which is > 0. "
                        f"Debuffs should have either a rate of 0 (for example, mark) or < 0 (for example, DEF down)"
                        f"\n{expected_info_single}")

    actual_info = [
        DebuffInfo(unit.hit_attr_label, unit.parameter, unit.rate, unit.probability_pct, unit.duration_time,
                   unit.stackable)
        for unit in actual_units
    ]

    check_info_list_match(actual_info, expected_info, message=message)
