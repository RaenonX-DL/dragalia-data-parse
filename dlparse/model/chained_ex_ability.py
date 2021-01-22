"""Models for chained ex ability data."""
from dataclasses import dataclass

from .ability import AbilityData

__all__ = ("ChainedExAbilityData",)


@dataclass
class ChainedExAbilityData(AbilityData):
    """A transformed chained ex ability data."""
