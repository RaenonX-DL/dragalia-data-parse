"""Hit execution type enum."""
from enum import IntEnum


class HitExecType(IntEnum):
    """Enum of the hit execution type."""

    UNKNOWN = -1

    DAMAGE = 1
    BUFF = 2

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
