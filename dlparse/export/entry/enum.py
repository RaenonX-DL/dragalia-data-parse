"""Enum entry classes for exporting."""
from dataclasses import dataclass
from typing import Any

from dlparse.enums import ColorTheme
from .base import JsonExportableEntryBase
from .text import TextEntry

__all__ = ("EnumEntry", "ConditionEnumEntry")


@dataclass
class EnumEntry(JsonExportableEntryBase):
    """Single entry of an enum to be used on the website."""

    enum_name: str
    enum_code: int
    enum_image_path: str

    trans: TextEntry

    def to_json_entry(self) -> dict[str, Any]:
        # Used by the website, DO NOT CHANGE
        return {
            "name": self.enum_name,
            "code": self.enum_code,
            "imagePath": self.enum_image_path,
            "trans": self.trans.to_json_entry()
        }


@dataclass
class ConditionEnumEntry(EnumEntry):
    """Single entry for a condition enum."""

    color_theme: ColorTheme  # Bootstrap color theme to be used on the website

    def to_json_entry(self) -> dict[str, Any]:
        # Used by the website, DO NOT CHANGE
        return super().to_json_entry() | {
            "colorTheme": self.color_theme.value,
        }
