"""Class for ``ActionPartsActiveCancel`` action component."""
from dataclasses import dataclass

from dlparse.enums import SkillCancelType
from dlparse.mono.asset.base import ActionComponentBase


@dataclass
class ActionActiveCancel(ActionComponentBase):
    """Class of ``ActionPartsActiveCancel`` component in the player action asset."""

    action_id: int
    cancel_type: SkillCancelType

    @property
    def has_specific_cancel_action(self) -> bool:
        """Check if the cancel action is conditional."""
        return self.action_id != 0

    @classmethod
    def parse_raw(cls, data: dict[str, int]) -> "ActionActiveCancel":
        kwargs = cls.get_base_kwargs(data)

        return ActionActiveCancel(
            action_id=data["_actionId"],
            cancel_type=SkillCancelType(data["_actionType"]),
            **kwargs
        )
