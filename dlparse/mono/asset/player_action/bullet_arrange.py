"""Class for arranged bullets (command type = 37)."""
from dataclasses import dataclass

from dlparse.mono.asset.base import ActionComponentData
from .bullet import ActionBullet

__all__ = ("ActionBulletArranged",)


@dataclass
class ActionBulletArranged(ActionBullet):
    """Class of arranged bullet component (command type = 37) in the player action asset."""

    @classmethod
    def parse_raw(cls, data: ActionComponentData) -> "ActionBulletArranged":
        kwargs = cls.get_base_kwargs(data)

        # Attach hit label of the bullet
        labels_possible: list[str] = [data["_abHitAttrLabel"]]

        return ActionBulletArranged(
            hit_labels=[label for label in labels_possible if label],
            bullet_duration=data["_abDuration"],
            collision_interval=data["_abHitInterval"],
            **kwargs
        )
