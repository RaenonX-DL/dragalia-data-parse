"""Character info model."""
from dataclasses import dataclass, field

from dlparse.enums import Weapon
from dlparse.mono.asset import CharaDataEntry
from .base import UnitInfo

__all__ = ("CharaInfo",)


@dataclass
class CharaInfo(UnitInfo[CharaDataEntry]):
    """Character info model."""

    weapon_type: Weapon = field(init=False)

    has_unique_dragon: bool = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.weapon_type = self.unit_entry.weapon
        self.has_unique_dragon = self.unit_entry.has_unique_dragon
