"""Class for ``ActionPartsMotion`` action component."""
from dataclasses import dataclass
from typing import Any, Union

from dlparse.mono.asset.base import ActionComponentBase


@dataclass
class ActionMotion(ActionComponentBase):
    """Class of ``ActionPartsMotion`` component in the player action asset."""

    motion_state: str

    @classmethod
    def parse_raw(cls, data: dict[str, Union[int, Any]]) -> "ActionMotion":
        kwargs = cls.get_base_kwargs(data)

        return ActionMotion(
            motion_state=data["_motionState"],
            **kwargs
        )
