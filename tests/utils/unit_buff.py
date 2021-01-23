"""Implementations for checking the buffing effects."""
from dataclasses import dataclass
from typing import Any

from dlparse.enums import BuffParameter, HitTargetSimple
from dlparse.model import HitActionConditionEffectUnit
from .unit_base import BuffInfoBase

__all__ = ("BuffEffectInfo", "check_buff_unit_match")


@dataclass
class BuffEffectInfo(BuffInfoBase):
    """A single buff effect info entry."""

    target: HitTargetSimple
    param: BuffParameter
    rate: float
    duration_time: float
    duration_count: float

    max_stack_count: int = 0

    def __hash__(self):
        return hash((self.target, self.param, self.rate, self.duration_time, self.duration_count, self.hit_label,
                     self.max_stack_count))


def check_buff_unit_match(
        actual_units: set[HitActionConditionEffectUnit], expected_info: set[BuffEffectInfo], /,
        check_stack_count: bool = False, message: Any = None
):
    """Check if the info of the buff units match."""
    actual_info = {
        BuffEffectInfo(unit.hit_attr_label, unit.target, unit.parameter, unit.rate, unit.duration_sec,
                       unit.duration_count, unit.max_stack_count if check_stack_count else 0)
        for unit in actual_units
    }

    # Message is hard-coded to let PyCharm display diff comparison tool
    expr_expected = "\\n".join([str(info) for info in sorted(expected_info)])
    expr_actual = "\\n".join([str(info) for info in sorted(actual_info)])

    assert_expr = f"assert {{{expr_actual}}} == {{{expr_expected}}}"

    if message is not None:
        assert_expr = f"{message}\n{assert_expr}"

    assert actual_info == expected_info, assert_expr  # nosec
