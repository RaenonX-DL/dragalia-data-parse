"""Entry of a simplified unit info."""
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING, TypeVar

from dlparse.mono.asset import UnitEntry
from . import JsonSchema
from .base import JsonExportableEntryBase, TextEntry

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("SimpleUnitInfoEntry",)

T = TypeVar("T", bound=UnitEntry)


@dataclass
class SimpleUnitInfoEntry(JsonExportableEntryBase):
    """
    A simple unit info entry.

    This will be used on every load of the website,
    therefore the amount of info included should be as less as possible.
    """

    asset_manager: "AssetManager"

    unit_data: T

    unit_name: TextEntry = field(init=False)

    def __post_init__(self):
        self.unit_name = TextEntry(
            asset_text_website=self.asset_manager.asset_text_website,
            asset_text_multi=self.asset_manager.asset_text_multi,
            labels=self.unit_data.name_labels
        )

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "name": TextEntry.json_schema,
            "type": int,
            "icon": str,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "name": self.unit_name.to_json_entry(),
            "type": self.unit_data.unit_type.value,
            "icon": self.unit_data.icon_name,
        }
