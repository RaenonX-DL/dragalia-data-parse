"""Class for a single damage mod unit."""
from dataclasses import dataclass

from .buff_boost import BuffCountBoostData

__all__ = ("DamageModifierUnit",)


@dataclass
class DamageModifierUnit:
    """A single unit of a damage modifier (of a hit)."""

    original: float
    crisis: float
    counter: float
    """
    Damage modifier to be added if the user is damaged during skill casting.

    Note that this damage is element-neutral.
    The formula of this is simply ``damage received x counter damage modifier``.
    Any additional effects such as crisis mods, punishers will **NOT** be applied.
    """

    buff_boost_data: BuffCountBoostData
