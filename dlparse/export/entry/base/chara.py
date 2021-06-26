"""Base class of an entry related to a character."""
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from dlparse.enums import Element
from .entry import JsonExportableEntryBase
from .text import TextEntry
from .type import JsonSchema

if TYPE_CHECKING:
    from dlparse.mono.asset import CharaDataEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("CharaEntryBase",)


@dataclass
class CharaEntryBase(JsonExportableEntryBase, ABC):
    """Base class for an exporting data entry that is bound to a certain character."""

    asset_manager: "AssetManager"

    chara_data: "CharaDataEntry"

    character_name: TextEntry = field(init=False)
    character_icon_name: str = field(init=False)
    character_internal_id: int = field(init=False)
    character_element: Element = field(init=False)

    def __post_init__(self):
        self.character_name = TextEntry(self.asset_manager.asset_text_multi, self.chara_data.name_labels)
        self.character_icon_name = self.chara_data.icon_name
        self.character_internal_id = self.chara_data.id
        self.character_element = self.chara_data.element

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
            "id": self.character_internal_id,
            "iconName": self.character_icon_name,
            "name": self.character_name.to_json_entry(),
            "element": self.character_element.value,
        }
