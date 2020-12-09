"""Hit execution type enum."""
from enum import IntEnum


class HitExecType(IntEnum):
    """
    Enums of the hit execution type.

    This corresponds to the field ``_HitExecType`` in the hit attribute asset.
    """

    UNKNOWN = -1

    DAMAGE = 1
    BUFF = 2
    GAUGE_REFILL = 7

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
