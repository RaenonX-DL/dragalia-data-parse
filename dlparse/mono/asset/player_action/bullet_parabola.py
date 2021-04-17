"""Class for ``ActionPartsParabolaBullet`` action component."""
from dataclasses import dataclass

from dlparse.mono.asset.base import ActionComponentData
from .bullet import ActionBullet
from .bullet_arrange import ActionBulletArranged

__all__ = ("ActionBulletParabola",)


@dataclass
class ActionBulletParabola(ActionBullet):
    """
    Class of ``ActionPartsParabolaBullet`` component in the player action asset.

    .. note::
        This component appears to not have a sub hit label field (``_hitAttrLabelSubList``)
        and deterioration rate (``_attenuationRate``).
    """

    @classmethod
    def parse_raw(cls, data: ActionComponentData) -> "ActionBullet":
        kwargs = cls.get_base_kwargs(data)

        # Main hit labels
        labels_possible: list[str] = [data["_hitAttrLabel"]]

        # Labels in arrange bullet
        if "_arrangeBullet" in data:
            labels_possible.extend(ActionBulletArranged.parse_raw(data["_arrangeBullet"]).hit_labels)

        return ActionBullet(
            hit_labels=[label for label in labels_possible if label],
            **kwargs
        )
