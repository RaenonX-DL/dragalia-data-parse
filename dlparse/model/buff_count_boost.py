"""Buff count boost data model."""
from dataclasses import dataclass

__all__ = ("BuffCountBoostData",)


@dataclass
class BuffCountBoostData:
    """Data used for calculating the damage boost according to the buff count."""

    in_effect_rate: float  # 0 = nothing in-effect
    """Rate of the buff boost already in-effect."""

    rate_limit: float  # 0 = unlimited
    """Maximum rate allowed."""
    rate_base: float  # 0 = no boost by buff count
    """Boost rate increase for each count of buffs."""

    action_condition_id: int  # 0 = not applicable
    """Action condition which has an enhanced boost rate."""
    action_condition_count_max: int  # 0 = uncapped
    """Maximum count of the action condition instances allowed."""
    action_condition_rate_each: float
    """Boost rate increase for each instance of the action condition."""

    def __hash__(self):
        # x 1E5 for handling floating errors
        return hash((
            int(self.in_effect_rate * 1E5), int(self.rate_limit * 1E5), int(self.rate_base * 1E5),
            self.action_condition_id, self.action_condition_count_max, int(self.action_condition_rate_each * 1E5)
        ))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return hash(self) == hash(other)
