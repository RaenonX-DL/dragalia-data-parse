"""
Enums for ability variant.

Check ``notes/enums/AbilityVariant.md`` for more details.
"""
from enum import Enum

__all__ = ("AbilityVariantType",)


class AbilityVariantType(Enum):
    """
    Enum class for the ability variant types.

    This corresponds to the field ``_AbilityTypeN`` in the ability data asset.

    Check ``notes/enums/AbilityVariant.md`` for more details.
    """

    UNKNOWN = -1

    NOT_USED = 0
    """Variant not used."""

    STATUS_UP = 1
    """Raise a certain status."""

    RESISTANCE_UP = 2
    """Raise the resistance toward a certain affliction."""

    CHANGE_STATE = 14
    """Calls the hit attribute (at str field) or the action condition (ID at ID-A field) if the condition holds."""

    SP_CHARGE = 17
    """Charge the SP gauges."""

    GAUGE_STATUS = 40
    """Grants different effects according to the user's gauge status."""

    OTHER_ABILITY = 43
    """Link to another ability (at ID-A field)."""

    ENHANCE_SKILL = 44
    """Enhance a skill (ID at ID-A field, # at target action field)."""

    DMG_UP_ON_COMBO = 54
    """Damage up by user combo count."""

    REMOVE_ALL_STOCK_BULLETS = 60
    """Remove all stock bullets."""

    @classmethod
    def _missing_(cls, _):
        return AbilityVariantType.UNKNOWN
