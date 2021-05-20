"""Interface for various types of units. This includes character and dragon."""
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar

from dlparse.enums import Element
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase
from .named import NamedEntry
from .varied import VariedEntry

__all__ = ("UnitEntry", "UnitAsset")


@dataclass
class UnitEntry(NamedEntry, VariedEntry, MasterEntryBase, ABC):
    """Interface for an unit."""

    element: Element
    rarity: int

    cv_en_label: str
    cv_jp_label: str

    release_date: datetime

    is_playable: bool

    @property
    def icon_name(self) -> str:
        """Get the name of the character icon, excluding the file extension."""
        return f"{self.base_id}_{self.variation_id:02}_r{self.rarity:02}"


T = TypeVar("T", bound=UnitEntry)


class UnitAsset(Generic[T], MasterAssetBase[T], ABC):
    """Interface for an asset that contains unit entries."""

    @property
    def playable_data(self) -> list[T]:
        """Get all playable units.."""
        return [data for data in self if data.is_playable]
