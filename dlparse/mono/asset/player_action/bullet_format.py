"""Class for ``ActionPartsFormationBullet`` action component."""
from dataclasses import dataclass
from typing import Any

from .bullet import ActionBullet
from .bullet_arrange import ActionBulletArranged

__all__ = ("ActionBulletFormation",)


@dataclass
class ActionBulletFormation(ActionBullet):
    """
    Class of ``ActionPartsFormationBullet`` component in the player action asset.

    .. note::
        As of 2021/07/26, only the following skills are using this component:

        - Yukata Curran S2 Masked (``103504044``)

        - OG!Zena S2 (``107505042``)

        - Megaman S2 effective normal attack (Mode 2, combo ID ``799200``, unit ID ``10750102``)
    """

    def __post_init__(self):
        self.hit_labels = self.hit_labels * (self.max_hit_count or 1)  # Single bullet can hit multiple times

    @classmethod
    def parse_raw(cls, data: dict[str, Any]) -> "ActionBulletFormation":
        kwargs = cls.get_base_kwargs(data)

        # Attach hit labels of the stock bullets
        labels_possible: list[str] = [data["_hitAttrLabel"]] + data["_hitAttrLabelSubList"]

        # Labels in arrange bullet
        if "_arrangeBullet" in data:
            labels_possible.extend(ActionBulletArranged.parse_raw(data["_arrangeBullet"]).hit_labels)

        # Attach hit labels of the child bullets
        for child_idx in range(data["_childNum"]):
            labels_possible.extend(ActionBullet.parse_raw(data["_child"][child_idx]["bulletData"]).hit_labels)

        return ActionBulletFormation(
            hit_labels=[label for label in labels_possible if label],
            **kwargs
        )
