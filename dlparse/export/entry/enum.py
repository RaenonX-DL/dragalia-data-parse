"""Enum entry classes for exporting."""
from dataclasses import dataclass
from typing import Any

from dlparse.enums import ColorTheme
from .base import JsonSchema, NamedEntry

__all__ = ("EnumEntry", "ConditionEnumEntry")


@dataclass
class EnumEntry(NamedEntry):
    """Single entry of an enum to be used on the website."""

    code: int
    image_path: str

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return super().json_schema | {
            "code": str,
            "imagePath": str
        }

    def to_json_entry(self) -> dict[str, Any]:
        return super().to_json_entry() | {
            "code": self.code,
            "imagePath": self.image_path
        }


@dataclass
class ConditionEnumEntry(EnumEntry):
    """Single entry for a condition enum."""

    color_theme: ColorTheme  # Bootstrap color theme to be used on the website

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return super().json_schema | {
            "colorTheme": str,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return super().to_json_entry() | {
            "colorTheme": self.color_theme.value,
        }
