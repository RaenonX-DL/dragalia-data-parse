"""Base classes of an effect unit."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from dlparse.enums import BuffParameter, HitTargetSimple, Status

__all__ = ("EffectUnitBase",)


@dataclass
class EffectUnitBase(ABC):
    """Base class of the effect units."""

    status: Status

    target: HitTargetSimple
    parameter: BuffParameter
    probability_pct: float  # 90 = 90%
    rate: float

    slip_interval: float
    slip_damage_mod: float

    duration_time: float
    duration_count: float

    max_stack_count: int
    """
    Maximum count of the buffs stackable.

    ``0`` means not applicable (``duration_count`` = 0, most likely is a buff limited by time duration).

    ``1`` means unstackable.

    Any positive number means the maximum count of stacks possible.
    """

    @property
    def stackable(self):
        """Check if the effect unit is stackable."""
        return self.max_stack_count != 1

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError()
