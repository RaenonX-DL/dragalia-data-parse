"""Entry of an unit info."""
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, TYPE_CHECKING, TypeVar

from dlparse.enums import Element
from dlparse.mono.asset import UnitEntry
from .entry import JsonExportableEntryBase
from .text import TextEntry
from .type import JsonSchema

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("UnitInfoEntryBase",)

T = TypeVar("T", bound=UnitEntry)


@dataclass
class UnitInfoEntryBase(Generic[T], JsonExportableEntryBase, ABC):
    """Base class of an unit info entry."""

    asset_manager: "AssetManager"

    unit_data: T

    unit_name: TextEntry = field(init=False)
    unit_icon_name: str = field(init=False)
    unit_id: int = field(init=False)
    unit_element: Element = field(init=False)
    unit_rarity: int = field(init=False)
    unit_cv_en: TextEntry = field(init=False)
    unit_cv_jp: TextEntry = field(init=False)
    unit_release_date: datetime = field(init=False)

    def __post_init__(self):
        self.unit_name = TextEntry(self.asset_manager.asset_text_multi, self.unit_data.name_labels)
        self.unit_icon_name = self.unit_data.icon_name
        self.unit_id = self.unit_data.id
        self.unit_element = self.unit_data.element
        self.unit_rarity = self.unit_data.rarity
        self.unit_cv_en = TextEntry(self.asset_manager.asset_text_multi, self.unit_data.cv_en_label)
        self.unit_cv_jp = TextEntry(self.asset_manager.asset_text_multi, self.unit_data.cv_jp_label)
        self.unit_release_date = self.unit_data.release_date

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "name": TextEntry.json_schema,
            "iconName": str,
            "id": int,
            "element": int,
            "rarity": int,
            "cvEn": TextEntry.json_schema,
            "cvJp": TextEntry.json_schema,
            "releaseEpoch": float,
            "type": int,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "name": self.unit_name.to_json_entry(),
            "iconName": self.unit_icon_name,
            "id": self.unit_id,
            "element": self.unit_element.value,
            "rarity": self.unit_rarity,
            "cvEn": self.unit_cv_en.to_json_entry(),
            "cvJp": self.unit_cv_jp.to_json_entry(),
            "releaseEpoch": self.unit_release_date.timestamp(),
            "type": self.unit_data.unit_type.value,
        }
