"""Class for ``ActionPartsActiveCancel`` action component."""
from dataclasses import dataclass

from dlparse.mono.asset.base import ActionComponentBase


@dataclass
class ActionActiveCancel(ActionComponentBase):
    """Class of ``ActionPartsActiveCancel`` component in the player action asset."""

    action_id: int

    @property
    def has_specific_cancel_action(self) -> bool:
        """Check if the cancel action is conditional."""
        return self.action_id != 0

    @classmethod
    def parse_raw(cls, data: dict[str, int]) -> "ActionActiveCancel":
        kwargs = cls.get_base_kwargs(data)

        return ActionActiveCancel(
            action_id=data["_actionId"],
            **kwargs
        )
