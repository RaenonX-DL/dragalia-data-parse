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

    CHANGE_STATE = 14
    """Calls the hit attribute (at str field) or the action condition (ID at ID-A field) if the condition holds."""

    OTHER_ABILITY = 43
    """Link to another ability (at ID-A field)."""

    ENHANCE_SKILL = 44
    """Enhance a skill (ID at ID-A field, # at target action field)."""

    DMG_UP_ON_COMBO = 54
    """Damage up by user combo count."""

    @classmethod
    def _missing_(cls, _):
        return AbilityVariantType.UNKNOWN
