"""Enum entry classes for exporting."""
from dataclasses import dataclass
from typing import Any

from .base import JsonExportableBase

__all__ = ("EnumEntry",)


@dataclass
class EnumEntry(JsonExportableBase):
    """Single entry of an enum to be used on the website."""

    enum_name: str
    enum_code: int

    trans: dict[str, str]

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "name": self.enum_name,
            "code": self.enum_code,
            "trans": self.trans
        }
