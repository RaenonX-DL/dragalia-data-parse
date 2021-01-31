"""Classes for the effects of an action condition."""
from dataclasses import dataclass, field

from .base import EffectUnitBase

__all__ = ("HitActionConditionEffectUnit", "EnemyAfflictionEffectUnit")


@dataclass(eq=False)
class HitActionConditionEffectUnit(EffectUnitBase):
    """The smallest unit of an effect of an action condition coming from a hit attribute."""

    time: float

    hit_attr_label: str
    action_cond_id: int

    def __hash__(self):
        # Same hit attribute label may be used multiple times at different time
        # Action condition ID not included because it's bound with hit attribute label
        # x 1E5 for handling floating errors
        return hash((int(self.time * 1E5), self.hit_attr_label))

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError(f"Cannot compare `HitActionConditionEffectUnit` with {type(other)}")

        return self.time < other.time


@dataclass
class EnemyAfflictionEffectUnit(HitActionConditionEffectUnit):
    """An action condition effect that afflicts the enemy."""

    rate: float = field(init=False)
    duration_count: float = field(init=False)

    def __post_init__(self):
        # Directly sets the default causes error
        self.rate = 0
        self.duration_count = 0
