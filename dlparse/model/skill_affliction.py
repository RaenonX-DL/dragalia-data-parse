"""Class for a single affliction."""
from dataclasses import dataclass

from dlparse.enums import Status

__all__ = ("SkillAfflictionUnit",)


@dataclass
class SkillAfflictionUnit:
    """A unit of the skill affliction."""

    status: Status
    time: float
    rate_percent: float  # 90 = 90%
    duration: float
    interval: float
    damage_mod: float

    stackable: bool

    hit_attr_label: str
    action_cond_id: int

    def __hash__(self):
        # Same hit attribute label may be used multiple times at different time
        # x 1E5 for handling floating errors
        return hash((int(self.time * 1E5), self.hit_attr_label, self.action_cond_id))

    def __eq__(self, other):
        if not isinstance(other, SkillAfflictionUnit):
            return False

        return hash(self) == hash(other)

    def __lt__(self, other):
        if not isinstance(other, SkillAfflictionUnit):
            raise TypeError(f"Cannot compare `SkillAfflictionUnit` with type {type(other)}")

        return self.time < other.time
