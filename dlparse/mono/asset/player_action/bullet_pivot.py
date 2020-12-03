"""Class for ``ActionPartsPivotBullet`` action component."""
from dataclasses import dataclass
from typing import Union

from .bullet import ActionBullet
from .bullet_arrange import ActionBulletArranged

__all__ = ("ActionBulletPivot",)


@dataclass
class ActionBulletPivot(ActionBullet):
    """Class of ``ActionPartsPivotBullet`` component in the player action asset."""

    @classmethod
    def parse_raw(cls, data: dict[str, Union[int, str, dict[str, str]]]) -> "ActionBulletPivot":
        kwargs = cls.get_base_kwargs(data)

        # Calculate count of hits
        # A hit will be made at the initial time, then deal hits by a certain interval within the given duration
        hits = int(kwargs["time_duration"] // data["_collisionHitInterval"]) + 1

        # Attach hit labels
        labels_possible: list[str] = [data["_hitAttrLabel"]] * hits

        # Labels in arrange bullet
        if "_arrangeBullet" in data:
            labels_possible.extend(ActionBulletArranged.parse_raw(data["_arrangeBullet"]).hit_labels)

        return ActionBulletPivot(
            hit_labels=[label for label in labels_possible if label],
            **kwargs
        )
