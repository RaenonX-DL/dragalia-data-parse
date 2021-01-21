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

    SKILL_DMG_UP = 6
    """Raise the character's skill damage. If the variant is inside an ex ability entry, the effect is team-wide."""

    CRT_RATE_UP = 7
    """Raise the character's CRT rate. If the variant is inside an ex ability entry, the effect is team-wide."""

    RP_UP = 8
    """
    Raise the character's Recovery Potency of their skills.

    If the variant is inside an ex ability entry, the effect is team-wide.
    """

    OD_GAUGE_DMG_UP = 9
    """Raise the damage toward the OD gauge. If the variant is inside an ex ability entry, the effect is team-wide."""

    CHANGE_STATE = 14
    """Calls the hit attribute (at str field) or the action condition (ID at ID-A field) if the condition holds."""

    SP_CHARGE = 17
    """Charge the SP gauges."""

    PLAYER_EXP_UP = 21
    """Raises the player EXP gain upon clearing a quest."""

    ACTION_GRANT = 25
    """Grant a action condition to a specific action."""

    GAUGE_STATUS = 40
    """Grants different effects according to the user's gauge status."""

    HIT_ATTR_SHIFT = 42
    """Shifts the hit attributes."""

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
