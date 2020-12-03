"""Class for ``ActionPartsFireStockBullet`` action component."""
from dataclasses import dataclass
from typing import Union

from dlparse.enums import FireStockPattern
from dlparse.errors import BulletMaxCountUnavailableError
from .bullet import ActionBullet
from .bullet_arrange import ActionBulletArranged

__all__ = ("ActionBulletStockFire",)


@dataclass
class ActionBulletStockFire(ActionBullet):
    """Class of ``ActionPartsFireStockBullet`` component in the player action asset."""

    is_user_buff_count_dependent: bool = False

    @classmethod
    def parse_raw(cls, data: dict[str, Union[int, str, dict[str, str]]]) -> "ActionBulletStockFire":
        kwargs = cls.get_base_kwargs(data)

        # Get the bullet stocking pattern
        pattern = FireStockPattern(data["_fireStockPattern"])

        # Attach hit labels of the stock bullets
        labels_possible: list[str]
        if pattern == FireStockPattern.USER_BUFF_COUNT_DEPENDENT:
            # -- Hit is buff dependent, do **NOT** expand the hit labels
            # Handle hit count during skill data processing instead,
            # because player action info and skill condition are required to get the actual mods
            labels_possible = [data["_hitAttrLabel"]]
        else:
            # -- Normal case
            # This assumes ``_hitAttrLabel2nd`` is not duplicated by ``_bulletNum``
            labels_possible = [data["_hitAttrLabel"]] * data["_bulletNum"] + [data["_hitAttrLabel2nd"]]

        # Attach labels in arrange bullet
        if "_arrangeBullet" in data:
            labels_possible.extend(ActionBulletArranged.parse_raw(data["_arrangeBullet"]).hit_labels)

        return ActionBulletStockFire(
            hit_labels=[label for label in labels_possible if label],
            is_user_buff_count_dependent=pattern == FireStockPattern.USER_BUFF_COUNT_DEPENDENT,
            **kwargs
        )

    @property
    def max_hit_count(self) -> int:
        if self.is_user_buff_count_dependent:
            raise BulletMaxCountUnavailableError("Action data info is needed to get the actual max bullet count")

        return super().max_hit_count
