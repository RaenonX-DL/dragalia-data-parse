"""Skill canceling action data unit."""
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, Union

from dlparse.enums import ConditionComposite, SkillCancelAction
from dlparse.mono.loader import MotionLoaderBase

if TYPE_CHECKING:
    from dlparse.mono.asset import CharaDataEntry, DragonDataEntry, PlayerActionPrefab

__all__ = ("SkillCancelActionUnit",)

T = TypeVar("T", bound=MotionLoaderBase)


@dataclass
class SkillCancelActionUnit:
    """Unit of the skill canceling action."""

    action: SkillCancelAction
    time: float

    pre_conditions: ConditionComposite

    @staticmethod
    def from_player_action_prefab(
            motion_loader: T, data_entry: Union["CharaDataEntry", "DragonDataEntry"], prefab: "PlayerActionPrefab",
            pre_conditions: ConditionComposite = ConditionComposite()
    ) -> list["SkillCancelActionUnit"]:
        """Get the skill cancel action units from the player action prefab."""
        cancel_units: list[SkillCancelActionUnit] = []

        for cancel_action in prefab.cancel_actions:
            cancel_units.append(SkillCancelActionUnit(
                action=SkillCancelAction(cancel_action.action_id),
                time=cancel_action.time_start,
                pre_conditions=pre_conditions
            ))

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
                action=SkillCancelAction.MOTION_ENDS, time=end_time, pre_conditions=pre_conditions
            ))

        return cancel_units
