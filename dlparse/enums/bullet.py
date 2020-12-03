"""Enums of the fields in bullet action components."""
from enum import Enum

__all__ = ("FireStockPattern",)


class FireStockPattern(Enum):
    """
    Fire stock pattern enums.

    This exists in the field ``_fireStockPattern`` of ``ActionPartsFireStockBullet`` (:class:`ActionBulletStockFire`).
    """

    UNKNOWN = -1

    USER_BUFF_COUNT_DEPENDENT = 2

    @classmethod
    def _missing_(cls, _):
        return FireStockPattern.UNKNOWN
