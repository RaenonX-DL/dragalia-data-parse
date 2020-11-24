"""Player action component type."""
from enum import Enum

__all__ = ("ActionCommandType",)


class ActionCommandType(Enum):
    """
    Enums for action command type.

    The number corresponds to the ``commandType`` fields in the player action assets.
    """

    BULLET = 9
    """For ``$Script`` = ``ActionPartsBullet``."""
    HIT = 10
    """For ``$Script`` = ``ActionPartsHit``."""
    BULLET_ARRANGE = 37
    """Arranged bullet. Seen in ``_additionalCollision`` and ``_arrangeBullet``."""
    BULLET_STOCK = 59
    """For ``$Script`` = ``ActionPartsFireStockBullet``."""
    BULLET_FORMATION = 100
    """For ``$Script`` = ``ActionPartsFormationBullet``."""
