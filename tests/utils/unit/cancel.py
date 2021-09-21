"""Implementations for checking the cancel units."""
from dataclasses import dataclass
from typing import Any, Sequence

from dlparse.enums import SkillCancelAction
from dlparse.model import SkillCancelActionUnit
from .base import InfoBase, check_info_list_match

__all__ = ("CancelUnitInfo", "check_cancel_unit_match")


@dataclass(eq=False)
class CancelUnitInfo(InfoBase):
    """A single cancel info entry."""

    action: SkillCancelAction
    time: float

    @property
    def _comparer(self) -> tuple[Any, ...]:
        return int(round(self.time * 1E5)), self.action


def check_cancel_unit_match(
        actual_units: Sequence[SkillCancelActionUnit], expected_info: list[CancelUnitInfo], /,
        message: Any = None
) -> None:
    """Check if the info of the cancel units match."""
    actual_info = [CancelUnitInfo(unit.action, unit.time) for unit in actual_units]

    check_info_list_match(actual_info, expected_info, message=message)
