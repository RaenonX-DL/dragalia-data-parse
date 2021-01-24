"""Exporting entry for a skill identifier info."""
from dataclasses import dataclass
from typing import Any

from .base import JsonExportableEntryBase, TextEntry

__all__ = ("SkillIdentifierEntry",)


@dataclass
class SkillIdentifierEntry(JsonExportableEntryBase):
    """A single entry of a skill identifier info."""

    name: str
    trans: TextEntry

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "trans": self.trans.to_json_entry()
        }
