"""Skill canceling action data unit."""
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, TypeVar

from dlparse.enums import ConditionComposite, SkillCancelAction, SkillCancelType
from dlparse.mono.loader import MotionLoaderBase

if TYPE_CHECKING:
    from dlparse.mono.asset import PlayerActionPrefab, UnitEntry

__all__ = ("SkillCancelActionUnit",)

T = TypeVar("T", bound=MotionLoaderBase)


@dataclass
class SkillCancelActionUnit:
    """Unit of the skill canceling action."""

    action: SkillCancelAction
    action_id: Optional[int]
    cancel_type: SkillCancelType
    time: float

    pre_conditions: ConditionComposite

    @staticmethod
    def from_player_action_prefab(
            prefab: "PlayerActionPrefab",
            pre_conditions: ConditionComposite = ConditionComposite()
    ) -> list["SkillCancelActionUnit"]:
        """Get the skill cancel action units from ``prefab``."""
        cancel_units: list[SkillCancelActionUnit] = []

        for cancel_action in prefab.cancel_actions:
            cancel_units.append(SkillCancelActionUnit(
                action=SkillCancelAction(cancel_action.action_id),
                action_id=cancel_action.action_id or None,
                cancel_type=cancel_action.cancel_type,
                time=cancel_action.time_start,
                pre_conditions=pre_conditions
            ))

        return cancel_units

    @staticmethod
    def from_player_action_motion(
            motion_loader: T, data_entry: "UnitEntry", prefab: "PlayerActionPrefab",
            pre_conditions: ConditionComposite = ConditionComposite()
    ) -> list["SkillCancelActionUnit"]:
        """Get the skill cancel action units from the player action prefab and the unit motion data."""
        cancel_units: list[SkillCancelActionUnit] = SkillCancelActionUnit.from_player_action_prefab(
            prefab, pre_conditions
        )

        # Only adds motion ends cancel unit if no active cancel components are available
        if not cancel_units:
            end_time = 0

            for motion in prefab.motions:
                end_time = max(
                    end_time,
                    motion.time_start + motion.time_duration,
                    motion_loader.get_motion_stop_time(data_entry, motion.motion_state)
                )

            cancel_units.append(SkillCancelActionUnit(
                action=SkillCancelAction.MOTION_ENDS,
                action_id=None,
                cancel_type=SkillCancelType.MOTION_ENDS,
                time=end_time,
                pre_conditions=pre_conditions
            ))

        return cancel_units
