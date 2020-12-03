"""Class for ``ActionPartsStockBullet`` action component."""
from dataclasses import dataclass
from typing import Union

from .bullet import ActionBullet
from .bullet_arrange import ActionBulletArranged

__all__ = ("ActionBulletStock",)


@dataclass
class ActionBulletStock(ActionBullet):
    """Class of ``ActionPartsStockBullet`` component in the player action asset."""

    @classmethod
    def parse_raw(cls, data: dict[str, Union[int, str, dict[str, str]]]) -> "ActionBulletStock":
        kwargs = cls.get_base_kwargs(data)

        # TEST: Check GaLaxi Fig Test

        # Attach hit labels of the stock bullets
        # This assumes ``_hitAttrLabel2nd`` is not duplicated by ``_bulletNum``
        labels_possible: list[str] = [data["_hitAttrLabel"]] * data["_bulletNum"] + [data["_hitAttrLabel2nd"]]

        # Labels in arrange bullet
        if "_arrangeBullet" in data:
            labels_possible.extend(ActionBulletArranged.parse_raw(data["_arrangeBullet"]).hit_labels)

        return ActionBulletStock(
            hit_labels=[label for label in labels_possible if label],
            **kwargs
        )
