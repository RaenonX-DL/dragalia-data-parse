"""Base class of an entry related to an unit."""
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from dlparse.enums import Element
from .entry import JsonExportableEntryBase
from .text import TextEntry
from .type import JsonSchema

if TYPE_CHECKING:
    from dlparse.mono.asset import UnitEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("UnitEntryBase",)


@dataclass
class UnitEntryBase(JsonExportableEntryBase, ABC):
    """Base class for an exporting data entry that is bound to a certain unit."""

    asset_manager: "AssetManager"

    unit_data: "UnitEntry"

    unit_name: TextEntry = field(init=False)
    unit_icon_name: str = field(init=False)
    unit_internal_id: int = field(init=False)
    unit_element: Element = field(init=False)

    def __post_init__(self):
        self.unit_name = TextEntry(self.asset_manager.asset_text_multi, self.unit_data.name_labels)
        self.unit_icon_name = self.unit_data.icon_name
        self.unit_internal_id = self.unit_data.id
        self.unit_element = self.unit_data.element

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "id": int,
            "iconName": str,
            "name": TextEntry.json_schema,
            "element": int,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "id": self.unit_internal_id,
            "iconName": self.unit_icon_name,
            "name": self.unit_name.to_json_entry(),
            "element": self.unit_element.value,
        }
