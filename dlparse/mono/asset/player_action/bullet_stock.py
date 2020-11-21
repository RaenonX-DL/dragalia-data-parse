"""Class for ``ActionPartsFireStockBullet`` action component."""
from dataclasses import dataclass
from typing import Union

from dlparse.mono.asset.base import ActionComponentBase, ActionComponentDamageDealerMixin

__all__ = ("ActionBulletStock",)


@dataclass
class ActionBulletStock(ActionComponentBase, ActionComponentDamageDealerMixin):
    """Class of ``ActionPartsFireStockBullet`` component in the player action asset."""

    @classmethod
    def parse_raw(cls, data: dict[str, Union[int, str, dict[str, str]]]) -> "ActionBulletStock":
        kwargs = cls.get_base_kwargs(data)

        # Attach hit labels of the stock bullets
        # This assumes ``_hitAttrLabel2nd`` is not duplicated by ``_bulletNum``
        labels_possible: list[str] = [data["_hitAttrLabel"]] * data["_bulletNum"] + [data["_hitAttrLabel2nd"]]

        # Labels in arrange bullet
        if "_arrangeBullet" in data:
            labels_possible.append(data["_arrangeBullet"]["_abHitAttrLabel"])

        return ActionBulletStock(
            hit_labels=[label for label in labels_possible if label],
            **kwargs
        )
