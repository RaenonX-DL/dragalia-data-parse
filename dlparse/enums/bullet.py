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
    BULLET_TRANSFORM_TO_SKILL = 4
    """
    Transform the bullets on the map to skill hits.

    Currently only used by Meene.

    - Meene S1 normal (`106503031`, AID `691190`)
    - Meene S2 normal (`106503032`, AID `691200`)
    - Meene S1 6+ butterflies variant (`106503033`, AID `691191`)
    - Meene S2 6+ butterflies variant (`106503036`, AID `691201`)
    """

    @classmethod
    def _missing_(cls, _):
        return FireStockPattern.UNKNOWN
