"""Various enums appear in the action components."""
from enum import Enum

__all__ = ("ActionCommandType", "ActionConditionType")


class ActionCommandType(Enum):
    """
    Enums for action command type.

    The number corresponds to the field ``commandType`` in the player action assets.
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


class ActionConditionType(Enum):
    """
    Enums for action component condition.

    This can be found in the field ``_conditionData._conditionType`` of every player action components.

    Check ``notes/assets/ActionComponentsCondition.md`` for more details.
    """

    UNIDENTIFIED = -1

    NONE = 0
    """The action component is always effective."""
    ACTION_CONDITION_COUNT = 1
    """The action component is effective only if the user has certain instances of the action condition."""
    ACTION_CANCEL = 6
    """The action component is effective only if it is executed to cancel the other action."""
    SEIMEI_SHIKIGAMI_LEVEL = 7
    """The action component effectiveness depends on Seimei's Shikigami level."""

    @classmethod
    def _missing_(cls, _):
        return ActionConditionType.UNIDENTIFIED
