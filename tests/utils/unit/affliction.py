"""Implementations for checking the affliction effects."""
from dataclasses import dataclass
from typing import Any

from dlparse.enums import Status
from dlparse.model import HitActionConditionEffectUnit
from .base import BuffInfoBase, check_info_list_match

__all__ = ("AfflictionInfo", "check_affliction_unit_match")


@dataclass(eq=False)
class AfflictionInfo(BuffInfoBase):
    """A single affliction info entry."""

    status: Status

    probability_pct: float  # 90 = 90%
    duration: float

    interval: float
    damage_mod: float

    stackable: bool

    @property
    def _comparer(self) -> tuple[Any, ...]:
        return (
            self.status,
            self.probability_pct,
            self.duration,
            int(round(self.interval * 1E5)),
            int(round(self.damage_mod * 1E5)),
            self.stackable
        )


def check_affliction_unit_match(
        actual_units: list[HitActionConditionEffectUnit], expected_info: list[AfflictionInfo], /,
        message: Any = None
) -> None:
    """Check if the info of the affliction units match."""
    actual_info = [
        AfflictionInfo(
            unit.hit_attr_label, unit.status, unit.probability_pct, unit.duration_sec,
            unit.slip_interval_sec, unit.slip_damage_mod, unit.stackable
        )
        for unit in actual_units
    ]

    check_info_list_match(actual_info, expected_info, message=message)
