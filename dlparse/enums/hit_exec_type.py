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
    NO_DAMAGE = 6  # Does not deal damage but target the enemy
    GAUGE_REFILL = 7

    @property
    def is_not_target_the_enemy(self) -> bool:
        """Returns ``true`` if the hit exec type indicates that the hit will not target the enemy."""
        return self in (HitExecType.BUFF, HitExecType.GAUGE_REFILL)

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
