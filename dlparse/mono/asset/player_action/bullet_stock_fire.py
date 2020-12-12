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

    pattern: FireStockPattern = FireStockPattern.NONE

    is_depends_on_bullet_summoned: bool = False
    is_depends_on_user_buff_count: bool = False
    is_depends_on_bullet_on_map: bool = False

    bullet_num: int = 0  # Used only if `pattern` is `FireStockPattern.BULLET_COUNT_SUMMONED`

    @classmethod
    def parse_raw(cls, data: dict[str, Union[int, str, dict[str, str]]]) -> "ActionBulletStockFire":
        kwargs = cls.get_base_kwargs(data)

        bullet_num: int = data["_bulletNum"]

        # Get the bullet stocking pattern
        pattern: FireStockPattern = FireStockPattern(data["_fireStockPattern"])

        # Attach hit labels of the stock bullets
        labels_possible: list[str]
        if pattern.is_special_pattern:
            # -- Special pattern - Hit count is independent, do **NOT** expand the hit labels
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
            pattern=pattern,
            is_depends_on_bullet_summoned=pattern == FireStockPattern.BULLET_COUNT_SUMMONED,
            is_depends_on_user_buff_count=pattern == FireStockPattern.USER_BUFF_COUNT_DEPENDENT,
            is_depends_on_bullet_on_map=pattern == FireStockPattern.BULLET_TRANSFORM_TO_SKILL,
            bullet_num=bullet_num,
            **kwargs
        )

    @property
    def is_special_pattern(self) -> bool:
        """Check if the bullet stock has a special pattern to fire."""
        return self.pattern.is_special_pattern

    @property
    def max_hit_count(self) -> int:
        if self.is_depends_on_user_buff_count:
            raise BulletMaxCountUnavailableError("This bullet is user buff count dependent. "
                                                 "Action data info is needed to get the actual max bullet count")

        if self.is_depends_on_bullet_on_map:
            raise BulletMaxCountUnavailableError("This depends on the count of bullets on the map. "
                                                 "Additional info is needed to get the actual max hit count.")

        if self.is_depends_on_bullet_summoned:
            return self.bullet_num

        return super().max_hit_count
