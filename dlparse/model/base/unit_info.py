"""Base implementations for unit info, such as character or dragon."""
from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from dlparse.enums import Element
from dlparse.mono.asset.extension import UnitEntry

__all__ = ("UnitInfo",)

T = TypeVar("T", bound=UnitEntry)


@dataclass
class UnitInfo(Generic[T], ABC):
    """Base unit info data model."""

    unit_entry: T

    unit_id: int = field(init=False)
    name_labels: list[str] = field(init=False)

    element: Element = field(init=False)
    rarity: int = field(init=False)

    cv_en_label: str = field(init=False)
    cv_jp_label: str = field(init=False)

    def __post_init__(self):
        self.unit_id = self.unit_entry.id
        self.name_labels = self.unit_entry.name_labels
        self.element = self.unit_entry.element
        self.rarity = self.unit_entry.rarity
        self.cv_en_label = self.unit_entry.cv_en_label
        self.cv_jp_label = self.unit_entry.cv_jp_label
