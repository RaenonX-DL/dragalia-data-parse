"""Enum entry classes for exporting."""
from dataclasses import dataclass
from typing import Any

from .base import JsonExportableEntryBase
from .text import TextEntry

__all__ = ("EnumEntry",)


@dataclass
class EnumEntry(JsonExportableEntryBase):
    """Single entry of an enum to be used on the website."""

    enum_name: str
    enum_code: int

    trans: TextEntry

    def to_json_entry(self) -> dict[str, Any]:
        # Synced with the website, DO NOT CHANGE
        return {
            "name": self.enum_name,
            "code": self.enum_code,
            "trans": self.trans.to_json_entry()
        }
