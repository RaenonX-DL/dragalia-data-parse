"""Classes for advanced dragon info entry."""
from dataclasses import dataclass

from dlparse.mono.asset import DragonDataEntry
from .common import AdvancedInfoEntryBase
from ..dragon_info import DragonInfoEntry

__all__ = ("DragonAdvancedData",)


@dataclass
class DragonAdvancedData(AdvancedInfoEntryBase[DragonInfoEntry, DragonDataEntry]):
    """An entry for the advanced info of a dragon."""
