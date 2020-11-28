"""Class for a single buffing hit."""
from dataclasses import dataclass
from typing import Optional

from dlparse.enums import HitTargetSimple
from dlparse.mono.asset import ActionComponentBase, ActionSettingHit, ActionConditionEntry
from .hit_base import HitData

__all__ = ("BuffingHitData",)


@dataclass
class BuffingHitData(HitData[ActionComponentBase]):
    """Class for the data of a single buffing hit."""

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
