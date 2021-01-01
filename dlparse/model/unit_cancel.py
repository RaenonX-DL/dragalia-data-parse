"""Skill canceling action data unit."""
from dataclasses import dataclass
from typing import TYPE_CHECKING

from dlparse.enums import SkillCancelAction

if TYPE_CHECKING:
    from dlparse.mono.asset import PlayerActionPrefab

__all__ = ("SkillCancelActionUnit",)


@dataclass
class SkillCancelActionUnit:
    """Unit of the skill canceling action."""

    action: SkillCancelAction
    time: float

    @staticmethod
    def from_player_action_prefab(prefab: "PlayerActionPrefab") -> list["SkillCancelActionUnit"]:
        """Get the skill cancel action units from the player action prefab."""
        cancel_units: list[SkillCancelActionUnit] = []

        for cancel_action in prefab.cancel_actions:
            cancel_units.append(SkillCancelActionUnit(
                action=SkillCancelAction(cancel_action.action_id),
                time=cancel_action.time_start
            ))

        return cancel_units
