"""Class for ``ActionPartsTerminateOtherParts`` action component."""
from dataclasses import dataclass
from typing import Any, Union

from dlparse.mono.asset.base import ActionComponentBase, ActionComponentCondition


@dataclass
class ActionTerminateOthers(ActionComponentBase):
    """Class of ``ActionPartsTerminateOtherParts`` component in the player action asset."""

    effective_condition: ActionComponentCondition

    @classmethod
    def parse_raw(cls, data: dict[str, Union[int, Any]]) -> "ActionTerminateOthers":
        kwargs = cls.get_base_kwargs(data)

        return ActionTerminateOthers(
            effective_condition=ActionComponentCondition.parse_raw(data["_partConditionData"]),
            **kwargs
        )
