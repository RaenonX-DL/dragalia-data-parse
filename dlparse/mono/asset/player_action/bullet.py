"""Class for ``ActionPartsBullet`` action component."""
from dataclasses import dataclass
from typing import Union

from dlparse.mono.asset.base import ActionComponentBase, ActionComponentDamageDealerMixin


@dataclass
class ActionBullet(ActionComponentBase, ActionComponentDamageDealerMixin):
    """Class of ``ActionPartsBullet`` component in the player action asset."""

    @classmethod
    def parse_raw(cls, data: dict[str, Union[str, dict[str, str]]]) -> "ActionBullet":
        kwargs = cls.get_base_kwargs(data)

        # Main hit labels
        labels_possible: list[str] = [data["_hitAttrLabel"], data["_hitAttrLabel2nd"]]

        # Labels in arrange bullet
        if "_arrangeBullet" in data:
            labels_possible.append(data["_arrangeBullet"]["_abHitAttrLabel"])

        return ActionBullet(
            hit_labels=[label for label in labels_possible if label],
            **kwargs
        )
