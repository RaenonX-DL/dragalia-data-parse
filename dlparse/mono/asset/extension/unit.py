"""Interface for various units. This includes character and dragon."""
from abc import ABC
from dataclasses import dataclass

from dlparse.enums import Element
from dlparse.mono.asset.base import MasterEntryBase
from .named import NamedEntry

__all__ = ("UnitEntry",)


@dataclass
class UnitEntry(NamedEntry, MasterEntryBase, ABC):
    """Interface for an unit."""

    element: Element
    rarity: int

    cv_en_label: str
    cv_jp_label: str
