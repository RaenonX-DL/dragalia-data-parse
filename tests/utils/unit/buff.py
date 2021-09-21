"""Implementations for checking the buffing effects."""
from dataclasses import dataclass
from itertools import zip_longest
from typing import Any

from dlparse.enums import BuffParameter, HitTargetSimple
from dlparse.model import HitActionConditionEffectUnit
from .base import BuffInfoBase

__all__ = ("BuffEffectInfo", "check_buff_unit_match")


@dataclass(eq=False)
class BuffEffectInfo(BuffInfoBase):
    """A single buff effect info entry."""

    target: HitTargetSimple
    param: BuffParameter
    rate: float
    duration_sec: float
    duration_count: float

    max_stack_count: int = 0

    @property
    def _comparer(self) -> tuple[Any, ...]:
        return (
            int(round(self.rate * 1E5)),
            self.duration_sec,
            self.duration_count,
            self.hit_label,
            self.max_stack_count
        )


def check_buff_unit_match(
        actual_units: set[HitActionConditionEffectUnit], expected_info: set[BuffEffectInfo], /,
        check_stack_count: bool = False, message: Any = None
) -> None:
    """Check if the info of the buff units match."""
    actual_info = {
        BuffEffectInfo(
            unit.hit_attr_label, unit.target, unit.parameter, unit.rate, unit.duration_sec,
            unit.duration_count, unit.max_stack_count if check_stack_count else 0
        )
        for unit in actual_units
    }

    expected_info = sorted(expected_info)
    actual_info = sorted(actual_info)

    # Message is hard-coded to let PyCharm display diff comparison tool
    expr_expected = "\\n".join([str(info) for info in expected_info])
    expr_actual = "\\n".join([str(info) for info in actual_info])

    assert_expr = f"assert {{{expr_actual}}} == {{{expr_expected}}}"

    if message is not None:
        assert_expr = f"{message}\n{assert_expr}"

    for idx, (actual, expected) in enumerate(zip_longest(actual_info, expected_info)):
        assert actual == expected, f"{assert_expr}\nIndex #{idx} not equal:"  # nosec
