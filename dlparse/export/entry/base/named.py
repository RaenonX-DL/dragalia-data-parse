"""Base entry of a named data."""
from dataclasses import dataclass
from typing import Any

from .entry import JsonExportableEntryBase
from .text import TextEntry
from .type import JsonSchema

__all__ = ("NamedEntry",)


@dataclass
class NamedEntry(JsonExportableEntryBase):
    """A single entry of a named data."""

    name: str
    trans: TextEntry

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "name": str,
            "trans": TextEntry.json_schema
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "trans": self.trans.to_json_entry()
        }
