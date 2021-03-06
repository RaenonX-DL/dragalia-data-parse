"""Base class for a single hit."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Optional, TYPE_CHECKING, TypeVar

from dlparse.enums import ConditionComposite, HitTargetSimple
from dlparse.mono.asset import (
    AbilityEntry, ActionBuffBomb, ActionComponentBase, ActionConditionEntry, ActionHit, ActionSettingHit, HitAttrEntry,
)

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("HitData", "T")

T = TypeVar("T", bound=ActionComponentBase)


@dataclass
class HitData(Generic[T], ABC):
    """Class for the data of a single hit."""

    hit_attr: HitAttrEntry
    action_id: int
    action_component: Optional[T]
    pre_condition_comp: ConditionComposite
    """
    Conditions for the hits to be effective.

    This may come from:
    - Condition from the action component
    - Ability condition embedded in the skill data
    """

    ability_data: list[AbilityEntry]
    action_cond_override: Optional[int] = None

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
            return HitTargetSimple.FIELD

        return ret

    @property
    def action_condition_id(self) -> int:
        """
        Get the actual action condition ID used for this hit data.

        If ``action_cond_override`` is specified, ``action_cond_override`` will be returned.
        Otherwise, action condition on ``hit_attr`` will be returned.
        """
        return self.action_cond_override or self.hit_attr.action_condition_id

    @abstractmethod
    def get_hit_count(
            self, original_hit_count: int, condition_comp: ConditionComposite, asset_manager: "AssetManager"
    ) -> int:
        """Get the total hit count of this hit."""
        raise NotImplementedError()

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

        # If the action component deploys a field, return its lifetime
        if isinstance(self.action_component, ActionSettingHit):
            return self.action_component.field_lifetime

        return 0
