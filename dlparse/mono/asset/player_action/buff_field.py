"""Class for ``ActionPartsBuffFieldAttachment`` action component."""
from dataclasses import dataclass

from dlparse.mono.asset.base import ActionComponentData, ActionComponentHasHitLabels

__all__ = ("ActionBuffField",)


@dataclass
class ActionBuffField(ActionComponentHasHitLabels):
    """Class of ``ActionPartsBuffFieldAttachment`` component in the player action asset."""

    count_for_self_built: bool

    @classmethod
    def parse_raw(cls, data: ActionComponentData) -> "ActionBuffField":
        kwargs = cls.get_base_kwargs(data)

        return ActionBuffField(
            hit_labels=[data["_hitAttrLabel"]],
            count_for_self_built=bool(data["_isAttachToSelfBuffField"]),
            **kwargs
        )
