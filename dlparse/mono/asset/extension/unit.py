"""Interface for various types of units. This includes character and dragon."""
from abc import ABC, abstractmethod
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
    @abstractmethod
    def icon_name(self) -> str:
        """Get the name of the icon, excluding the file extension."""
        raise NotImplementedError()


T = TypeVar("T", bound=UnitEntry)


class UnitAsset(Generic[T], MasterAssetBase[T], ABC):
    """Interface for an asset that contains unit entries."""

    @property
    def playable_data(self) -> list[T]:
        """Get all playable units.."""
        return [data for data in self if data.is_playable]
