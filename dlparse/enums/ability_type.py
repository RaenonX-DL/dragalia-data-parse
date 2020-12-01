"""Enums for ability type."""
from enum import Enum

__all__ = ("AbilityType",)


class AbilityType(Enum):
    """
    Enum class for ability type in the assets.

    This corresponds to the field ``_AbilityTypeN`` in the ability data asset.
    """

    UNKNOWN = -1

    TO_HIT_ATTR_ON_MATCH = 14
    """Link to the hit attribute label assigned (str field) if the condition holds."""

    TO_ABILITY_ON_MISMATCH = 43
    """Link to the ability assigned (id fields) if the condition fails."""

    @classmethod
    def _missing_(cls, _):
        return AbilityType.UNKNOWN
