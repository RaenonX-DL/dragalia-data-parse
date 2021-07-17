"""Classes for the EX (Co-ab) and chained EX (CCA) data entries."""
from dataclasses import dataclass, field
from typing import Any

from dlparse.mono.asset import CharaDataEntry
from .base import ExAbiltiesEntry, JsonExportableEntryBase, JsonSchema, UnitEntryBase

__all__ = ("CharaExAbiltiesEntry",)


@dataclass
class CharaExAbiltiesEntry(UnitEntryBase, JsonExportableEntryBase):
    """A single entry containing EX (Co-ab) and chained EX (CCA) of a character."""

    unit_data: CharaDataEntry

    ex_entry: ExAbiltiesEntry = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.ex_entry = ExAbiltiesEntry(asset_manager=self.asset_manager, unit_data=self.unit_data)

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        schema = {
            "chara": UnitEntryBase.json_schema
        }
        schema |= ExAbiltiesEntry.json_schema

        return schema

    def to_json_entry(self) -> dict[str, Any]:
        entry = {
            "chara": super().to_json_entry(),
        }
        entry |= self.ex_entry.to_json_entry()

        return entry
