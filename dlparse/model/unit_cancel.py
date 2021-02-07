"""Skill canceling action data unit."""
from dataclasses import dataclass
from typing import TYPE_CHECKING

from dlparse.enums import SkillCancelAction

if TYPE_CHECKING:
    from dlparse.mono.asset import CharaDataEntry, PlayerActionPrefab
    from dlparse.mono.loader import CharacterMotionLoader

__all__ = ("SkillCancelActionUnit",)


@dataclass
class SkillCancelActionUnit:
    """Unit of the skill canceling action."""

    action: SkillCancelAction
    time: float

    @staticmethod
    def from_player_action_prefab(
            chara_motion_loader: "CharacterMotionLoader", chara_data: "CharaDataEntry", prefab: "PlayerActionPrefab"
    ) -> list["SkillCancelActionUnit"]:
        """Get the skill cancel action units from the player action prefab."""
        cancel_units: list[SkillCancelActionUnit] = []

        for cancel_action in prefab.cancel_actions:
            cancel_units.append(SkillCancelActionUnit(
                action=SkillCancelAction(cancel_action.action_id),
                time=cancel_action.time_start
            ))

        # Only adds motion ends cancel unit if no active cancel components are available
        if not cancel_units:
            end_time = 0

            for motion in prefab.motions:
                end_time = max(
                    end_time,
                    motion.time_start + motion.time_duration,
                    chara_motion_loader.get_motion_stop_time(chara_data, motion.motion_state)
                )

            cancel_units.append(SkillCancelActionUnit(action=SkillCancelAction.MOTION_ENDS, time=end_time))

        return cancel_units
