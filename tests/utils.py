from dataclasses import dataclass
from typing import Any

import pytest

from dlparse.enums import BuffParameter, HitTargetSimple
from dlparse.model import ActionConditionEffectUnit

__all__ = ("approx_matrix", "BuffEffectInfo", "check_buff_unit_match")


def approx_matrix(data: list[list[float]]):
    """``pytest.approx()`` for a matrix."""
    return [pytest.approx(subdata) for subdata in data]


@dataclass
class BuffEffectInfo:
    """A single buff effect info entry."""

    target: HitTargetSimple
    param: BuffParameter
    rate: float
    duration_time: float
    duration_count: float
    hit_label: str

    max_stack_count: int = 0

    def __hash__(self):
        return hash((self.target, self.param, self.rate, self.duration_time, self.duration_count, self.hit_label,
                     self.max_stack_count))

    def __eq__(self, other):
        if not isinstance(other, BuffEffectInfo):
            return False

        return hash(self) == hash(other)

    def __lt__(self, other):
        if not isinstance(other, BuffEffectInfo):
            raise TypeError(f"Unable to compare `BuffEffectInfo` with {type(other)}")

        return self.hit_label < other.hit_label


def check_buff_unit_match(
        actual_units: set[ActionConditionEffectUnit], expected_info: set[BuffEffectInfo], /,
        check_stack_count: bool = False, message: Any = None
):
    """Check if the info of the buff units match."""
    actual_info = {
        BuffEffectInfo(unit.target, unit.parameter, unit.rate, unit.duration_time, unit.duration_count,
                       unit.hit_attr_label, unit.max_stack_count if check_stack_count else 0)
        for unit in actual_units
    }

    # Message is hard-coded to let PyCharm display diff comparison tool
    expr_expected = "\\n".join([str(info) for info in sorted(expected_info)])
    expr_actual = "\\n".join([str(info) for info in sorted(actual_info)])

    assert_expr = f"assert {expr_actual} == {expr_expected}"

    if message is not None:
        assert_expr = f"{message}\n{assert_expr}"

    assert actual_info == expected_info, assert_expr
