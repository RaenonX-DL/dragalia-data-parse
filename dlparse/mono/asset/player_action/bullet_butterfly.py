"""
Class for butterfly bullets (command type = 127).

Currently (2021/07/29) only used by Meene (10650303).
"""
from dataclasses import dataclass
from math import floor

from dlparse.mono.asset.base import ActionComponentData
from .bullet import ActionBullet

__all__ = ("ActionBulletButterfly",)


@dataclass
class ActionBulletButterfly(ActionBullet):
    """Class of arranged bullet component (command type = 37) in the player action asset."""

    @classmethod
    def parse_raw(cls, data: ActionComponentData) -> "ActionBulletButterfly":
        kwargs = cls.get_base_kwargs(data)

        # Bullet stays in the field for some time
        hit_count: int = max(floor(kwargs["bullet_duration"] / kwargs["collision_interval"]) + 1, 1)

        # Attach hit label of the bullet
        labels_possible: list[str] = [data["_hitAttrLabel"]] * hit_count

        return ActionBulletButterfly(
            hit_labels=[label for label in labels_possible if label],
            **kwargs
        )
