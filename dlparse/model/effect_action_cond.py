"""Classes for a single ability condition effect."""
from dataclasses import dataclass, field

from dlparse.enums import BuffParameter, HitTargetSimple, Status

__all__ = ("ActionConditionEffectUnit", "AfflictionEffectUnit")


@dataclass
class ActionConditionEffectUnit:
    """The atomic unit of an effect of an action condition."""

    time: float

    status: Status

    target: HitTargetSimple
    parameter: BuffParameter
    probability_pct: float  # 90 = 90%
    rate: float

    slip_interval: float
    slip_damage_mod: float

    duration_time: float
    duration_count: float

    hit_attr_label: str
    action_cond_id: int

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

    def __hash__(self):
        # Same hit attribute label may be used multiple times at different time
        # Action condition ID not included because it's bound with hit attribute label
        # x 1E5 for handling floating errors
        return hash((int(self.time * 1E5), self.hit_attr_label))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return hash(self) == hash(other)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError(f"Cannot compare `ActionConditionEffectUnit` with {type(other)}")

        return self.time < other.time


@dataclass
class AfflictionEffectUnit(ActionConditionEffectUnit):
    """An action condition effect that afflicts the enemy."""

    rate: float = field(init=False)
    duration_count: float = field(init=False)

    def __post_init__(self):
        # Directly sets the default causes error
        self.rate = 0
        self.duration_count = 0