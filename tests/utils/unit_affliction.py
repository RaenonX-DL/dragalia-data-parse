"""Implementations for checking the buff effects."""
from dataclasses import dataclass
from typing import Any

from dlparse.enums import Status
from dlparse.model import ActionConditionEffectUnit

__all__ = ("AfflictionInfo", "check_affliction_unit_match")


@dataclass
class AfflictionInfo:
    """A single affliction info entry."""

    status: Status

    probability_pct: float  # 90 = 90%
    duration: float

    interval: float
    damage_mod: float

    stackable: bool

    hit_label: str

    def __hash__(self):
        return hash((self.status, self.probability_pct, self.duration, self.interval, self.damage_mod, self.stackable,
                     self.hit_label))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return hash(self) == hash(other)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"Unable to compare {type(self.__class__)} with {type(other)}")

        return self.hit_label < other.hit_label


def check_affliction_unit_match(
        actual_units: list[ActionConditionEffectUnit], expected_info: list[AfflictionInfo], /,
        message: Any = None
):
    """Check if the info of the buff units match."""
    actual_info = [
        AfflictionInfo(unit.status, unit.probability_pct, unit.duration_time, unit.slip_interval, unit.slip_damage_mod,
                       unit.max_stack_count != 1, unit.hit_attr_label)
        for unit in actual_units
    ]

    # Message is hard-coded to let PyCharm display diff comparison tool
    expr_expected = "\\n".join([str(info) for info in sorted(expected_info)])
    expr_actual = "\\n".join([str(info) for info in sorted(actual_info)])

    assert_expr = f"assert [{expr_actual}] == [{expr_expected}]"

    if message is not None:
        assert_expr = f"{message}\n{assert_expr}"

    assert actual_info == expected_info, assert_expr
