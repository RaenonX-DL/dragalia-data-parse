"""Entry of a character info."""
from dataclasses import dataclass, field
from typing import Any

from dlparse.enums import Weapon
from dlparse.mono.asset import CharaDataEntry
from .base import JsonSchema, UnitInfoEntryBase

__all__ = ("CharaInfoEntry",)


@dataclass
class CharaInfoEntry(UnitInfoEntryBase[CharaDataEntry]):
    """Chara info entry class."""

    weapon: Weapon = field(init=False)

    has_unique_dragon: bool = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.weapon = self.unit_data.weapon
        self.has_unique_dragon = self.unit_data.has_unique_dragon

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return super().json_schema | {
            "weapon": int,
            "hasUniqueDragon": bool,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return super().to_json_entry() | {
            "weapon": self.weapon.value,
            "hasUniqueDragon": self.has_unique_dragon
        }
