"""Class for arranged bullets (command type = 37)."""
from dataclasses import dataclass
from typing import Union

from .bullet import ActionBullet

__all__ = ("ActionBulletArranged",)


@dataclass
class ActionBulletArranged(ActionBullet):
    """Class arranged bullet component (command type = 37) in the player action asset."""

    @classmethod
    def parse_raw(cls, data: dict[str, Union[int, str, dict[str, str]]]) -> "ActionBulletArranged":
        kwargs = cls.get_base_kwargs(data)

        # Attach hit label of the bullet
        labels_possible: list[str] = [data["_abHitAttrLabel"]]

        return ActionBulletArranged(
            hit_labels=[label for label in labels_possible if label],
            bullet_duration=data["_abDuration"],
            attenuation_rate=1,  # no attenuation
            collision_interval=data["_abHitInterval"],
            **kwargs
        )
