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
    """Buff a certain status."""

    RESISTANCE_UP = 2
    """Buff the resistance toward a certain affliction."""

    INFLICTION_PROB_UP = 3
    """Buff the infliction probability."""

    DAMAGE_UP = 6
    """Buff the target action damage. If the variant is inside an ex ability entry, the effect is team-wide."""

    CRT_RATE_UP = 7
    """Buff the character's CRT rate. If the variant is inside an ex ability entry, the effect is team-wide."""

    RP_UP = 8
    """
    Raise the character's Recovery Potency of their skills.

    If the variant is inside an ex ability entry, the effect is team-wide.
    """

    OD_GAUGE_DMG_UP = 9
    """Buff the damage toward the OD gauge. If the variant is inside an ex ability entry, the effect is team-wide."""

    CHANGE_STATE = 14
    """Call the hit attribute (at str field) or the action condition (ID at ID-A field) if the condition holds."""

    SP_CHARGE = 17
    """Charge the SP gauges."""

    BUFF_TIME_UP = 18
    """
    Extend the buff time.

    If the variant is inside an ex ability entry, the effect is team-wide.
    This only applies to the buffs that are directly applied to the user.
    Zoned buff like Gala Euden S1 (`10150403`) will not be affected by this.
    """

    AFFLICTION_PUNISHER = 20
    """Buff the damage dealt to the target if the target is afflicted by a certain affliction."""

    PLAYER_EXP_UP = 21
    """Buff the player EXP gain upon clearing a quest."""

    ACTION_GRANT = 25
    """Grant a action condition to a specific action."""

    CRT_DMG_UP = 26
    """Buff the character's CRT damage. If the variant is inside an ex ability entry, the effect is team-wide."""

    ELEM_RESIST_UP = 28
    """Buff the character's elemental damage resistance."""

    DRAGON_DMG_UP = 36
    """Buff the dragon damage."""

    GAUGE_STATUS = 40
    """Grant different effects according to the user's gauge status."""

    HIT_ATTR_SHIFT = 42
    """Shift the hit attributes."""

    OTHER_ABILITY = 43
    """Link to another ability (at ID-A field)."""

    ENHANCE_SKILL = 44
    """Enhance a skill (ID at ID-A field, # at target action field)."""

    FILL_DRAGON_GAUGE = 49
    """Fill the dragon gauge by a certain percentage."""

    DMG_UP_ON_COMBO = 54
    """Damage up by user combo count."""

    COMBO_TIME_EXT = 55
    """Extend the combo counter valid time."""

    ELEM_DMG_UP = 57
    """Buff the elemental damage."""

    REMOVE_ALL_STOCK_BULLETS = 60
    """Remove all stock bullets."""

    ADDITIONAL_HEAL_ON_REVIVE = 66
    """Receives additional healing based on the receiver's max HP."""

    @classmethod
    def _missing_(cls, _):
        return AbilityVariantType.UNKNOWN
