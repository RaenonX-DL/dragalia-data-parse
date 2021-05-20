"""Dragon info model."""
from dataclasses import dataclass

from dlparse.mono.asset import DragonDataEntry
from .base import UnitInfo

__all__ = ("DragonInfo",)


@dataclass
class DragonInfo(UnitInfo[DragonDataEntry]):
    """Dragon info model."""
