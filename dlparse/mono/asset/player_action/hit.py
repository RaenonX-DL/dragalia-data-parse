"""Class for ``ActionPartsHit`` action component."""
from dataclasses import dataclass

from dlparse.mono.asset.base import ActionComponentDamageDealer


@dataclass
class ActionHit(ActionComponentDamageDealer):
    """Class of ``ActionPartsHit`` component in the player action asset."""

    @classmethod
    def parse_raw(cls, data: dict[str, str]) -> "ActionHit":
        kwargs = cls.get_base_kwargs(data)

        return ActionHit(
            hit_labels=[data["_hitLabel"]],
            **kwargs
        )
