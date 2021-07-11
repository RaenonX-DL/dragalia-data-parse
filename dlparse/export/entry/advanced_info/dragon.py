"""Classes for advanced dragon info entry."""
from dataclasses import dataclass

from .common import AdvancedInfoEntryBase
from ..dragon_info import DragonInfoEntry

__all__ = ("DragonAdvancedData",)


@dataclass
class DragonAdvancedData(AdvancedInfoEntryBase[DragonInfoEntry]):
    """An entry for the advanced info of a dragon."""
