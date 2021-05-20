"""Entry of a dragon info."""
from dataclasses import dataclass

from dlparse.mono.asset import DragonDataEntry
from .base import UnitInfoEntryBase

__all__ = ("DragonInfoEntry",)


@dataclass
class DragonInfoEntry(UnitInfoEntryBase[DragonDataEntry]):
    """Dragon info entry class."""
