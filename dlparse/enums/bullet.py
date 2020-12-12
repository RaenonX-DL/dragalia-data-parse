"""Enums of the fields in bullet action components."""
from enum import Enum

__all__ = ("FireStockPattern",)


class FireStockPattern(Enum):
    """
    Fire stock pattern enums.

    This exists in the field ``_fireStockPattern`` of ``ActionPartsFireStockBullet`` (:class:`ActionBulletStockFire`).

    Check the documentation for ``ActionPartsFireStockBullet`` in ``notes/asset/ActionComponents.md`` for more details.
    """

    UNKNOWN = -1

    NONE = 0

    BULLET_COUNT_SUMMONED = 1
    USER_BUFF_COUNT_DEPENDENT = 2
    BULLET_TRANSFORM_TO_SKILL = 4

    @property
    def is_special_pattern(self):
        """Check if the fire stock pattern is a special pattern."""
        return self in (
            FireStockPattern.BULLET_COUNT_SUMMONED,
            FireStockPattern.USER_BUFF_COUNT_DEPENDENT,
            FireStockPattern.BULLET_TRANSFORM_TO_SKILL
        )

    @classmethod
    def _missing_(cls, _):
        return FireStockPattern.UNKNOWN
