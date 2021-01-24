"""Models for chained EX ability data."""
from dataclasses import dataclass

from .ability import AbilityData

__all__ = ("ChainedExAbilityData",)


@dataclass
class ChainedExAbilityData(AbilityData):
    """A transformed chained EX ability data."""

    is_chained_ex: bool = True
