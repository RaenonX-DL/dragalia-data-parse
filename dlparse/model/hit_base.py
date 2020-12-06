"""Base class for a single hit."""
from abc import ABC
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from dlparse.enums import HitTargetSimple, SkillCondition
from dlparse.mono.asset import ActionComponentBase, ActionConditionEntry, ActionSettingHit, HitAttrEntry

__all__ = ("HitData",)

T = TypeVar("T", bound=ActionComponentBase)


@dataclass
class HitData(Generic[T], ABC):
    """Class for the data of a single hit."""

    hit_attr: HitAttrEntry
    action_id: int
    action_component: Optional[T]
    pre_condition: SkillCondition
    """
    Condition for the hits to be effective.

    This may come from:
    - Condition from the action component
    - Ability condition embedded on the skill data
    """

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

    def get_duration(self, cond_entry: Optional[ActionConditionEntry]) -> float:
        """Get the duration of the buff."""
        # If action condition entry is available and it has duration set, return it
        if cond_entry and cond_entry.duration_sec:
            return cond_entry.duration_sec

        # If the action component sets an area, return its lifetime
        if isinstance(self.action_component, ActionSettingHit):
            return self.action_component.area_lifetime

        return 0
