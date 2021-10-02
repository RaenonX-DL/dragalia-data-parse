"""Class for ``ActionPartsHit`` action component."""
from dataclasses import dataclass
from typing import Union

from dlparse.mono.asset.base import ActionComponentHasHitLabels


@dataclass
class ActionHit(ActionComponentHasHitLabels):
    """Class of ``ActionPartsHit`` component in the player action asset."""

    hit_range: float

    @classmethod
    def parse_raw(cls, data: dict[str, Union[str, float]]) -> "ActionHit":
        kwargs = cls.get_base_kwargs(data)

        duration = kwargs["time_duration"]
        interval = data["_collisionHitInterval"]

        # +1 when interval is available for the initial hit
        hit_count = int(duration / interval) + 1 if interval else 1

        return ActionHit(
            hit_labels=[data["_hitLabel"]] * hit_count,
            hit_range=data["_collisionParams_01"],
            **kwargs
        )
