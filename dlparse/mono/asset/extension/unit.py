"""Interface for various units. This includes character and dragon."""
from abc import ABC
from dataclasses import dataclass
from datetime import datetime

from dlparse.enums import Element
from dlparse.mono.asset.base import MasterEntryBase
from .named import NamedEntry
from .varied import VariedEntry

__all__ = ("UnitEntry",)


@dataclass
class UnitEntry(NamedEntry, VariedEntry, MasterEntryBase, ABC):
    """Interface for an unit."""

    element: Element
    rarity: int

    cv_en_label: str
    cv_jp_label: str

    release_date: datetime

    @property
    def icon_name(self) -> str:
        """Get the name of the character icon, excluding the file extension."""
        return f"{self.base_id}_{self.variation_id:02}_r{self.rarity:02}"
