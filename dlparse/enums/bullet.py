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

    BULLET_COUNT_SUMMONED = 1  # StockBullet
    USER_BUFF_COUNT_DEPENDENT = 2  # BuffCount
    BULLET_TRANSFORM_TO_SKILL = 4  # ButterflyNum
    USER_BUFF_COUNT_DEPENDENT_EMBEDDED = 5  # DuplicatedBuffCount
    """
    The embedded here means that the maximum count of the bullets to fire
    is already embedded in the action parts data.
    """

    @property
    def is_special_pattern(self) -> bool:
        """
        Check if the fire stock pattern is a special pattern.

        Special pattern means that the actual bullet fire count depends on any other thing,
        such as how many bullets summoned on the map, how many buff the user has, etc.
        """
        return self in (
            FireStockPattern.BULLET_COUNT_SUMMONED,
            FireStockPattern.USER_BUFF_COUNT_DEPENDENT,
            FireStockPattern.USER_BUFF_COUNT_DEPENDENT_EMBEDDED,
            FireStockPattern.BULLET_TRANSFORM_TO_SKILL
        )

    @property
    def is_user_buff_count_dependent(self) -> bool:
        """Check if the stock bullet firing pattern depends on the user buff count."""
        return self in (
            FireStockPattern.USER_BUFF_COUNT_DEPENDENT,
            FireStockPattern.USER_BUFF_COUNT_DEPENDENT_EMBEDDED
        )

    @classmethod
    def _missing_(cls, _):
        return FireStockPattern.UNKNOWN
