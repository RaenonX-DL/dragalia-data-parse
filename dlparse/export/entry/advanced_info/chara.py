"""Classes for advanced character info entry."""
from dataclasses import dataclass

from .common import AdvancedInfoEntryBase
from ..chara_info import CharaInfoEntry

__all__ = ("CharaAdvancedData",)


@dataclass
class CharaAdvancedData(AdvancedInfoEntryBase[CharaInfoEntry]):
    """An entry for the advanced info of a character."""
