"""Base class for a single hit."""
from abc import ABC
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from dlparse.enums import Condition, HitTargetSimple
from dlparse.mono.asset import (
    AbilityEntry, ActionBuffBomb, ActionComponentBase, ActionConditionEntry, ActionHit, ActionSettingHit, HitAttrEntry,
)

__all__ = ("HitData", "T")

T = TypeVar("T", bound=ActionComponentBase)


@dataclass
class HitData(Generic[T], ABC):
    """Class for the data of a single hit."""

    hit_attr: HitAttrEntry
    action_id: int
    action_component: Optional[T]
    pre_condition: Condition
    """
    Condition for the hits to be effective.

    This may come from:
    - Condition from the action component
    - Ability condition embedded on the skill data
    """

    ability_data: list[AbilityEntry]

    @property
    def action_time(self):
        """Get the starting time of the action."""
        if not self.action_component:
            # Action component may be ``None`` if the hit directly comes from the ability
            # For example, skill -> ability
            return 0

        return self.action_component.time_start

    @property
    def target_simple(self) -> HitTargetSimple:
        """Simplified target of the buffing hit."""
        ret: HitTargetSimple = self.hit_attr.target_group.to_simple()

        if isinstance(self.action_component, ActionSettingHit) and ret == HitTargetSimple.SELF_SURROUNDING:
            return HitTargetSimple.AREA

        return ret

    def is_effective_to_enemy(self, desired_effectiveness: bool) -> bool:
        """
        Check if the hit is effective to the enemy.

        If any of the conditions below holds, the hit is considered effective:

        - Afflict the enemy

        - Deals damage to the enemy
        """
        if self.hit_attr.is_effective_to_enemy(desired_effectiveness):
            # Check if the action component is :class:`ActionHit`, if it is, verify it's range is not 0
            # > This happens on Lathna S1 (`105505021`) and Ramona S1 (`104501011`),
            # > where the last hit is only effective in Mercurial Gauntlet (last hit range = 0)
            if isinstance(self.action_component, ActionHit):
                return self.action_component.hit_range > 0

            # Otherwise, it's effective
            return True

        if isinstance(self.action_component, ActionBuffBomb):
            # Action component is buff bomb, targeted to the enemy
            return True

        return False

    def get_duration(self, cond_entry: Optional[ActionConditionEntry]) -> float:
        """Get the duration of the buff."""
        # If action condition entry is available and it has duration set, return it
        if cond_entry and cond_entry.duration_sec:
            return cond_entry.duration_sec

        # If the action component sets an area, return its lifetime
        if isinstance(self.action_component, ActionSettingHit):
            return self.action_component.area_lifetime

        return 0
