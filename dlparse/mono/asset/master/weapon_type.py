"""Classes for handling the weapon type asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import Weapon
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("WeaponTypeEntry", "WeaponTypeAsset")


@dataclass
class WeaponTypeEntry(MasterEntryBase):
    """Single entry of a weapon type data."""

    root_normal_attack_action_id: int

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "WeaponTypeEntry":
        return WeaponTypeEntry(
            id=data["_Id"],
            root_normal_attack_action_id=data["_DefaultSkill01"],
        )


class WeaponTypeAsset(MasterAssetBase[WeaponTypeEntry]):
    """Weapon type asset class."""

    asset_file_name = "WeaponType.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(WeaponTypeParser, file_location, asset_dir=asset_dir, file_like=file_like)

    def get_data_by_weapon(self, weapon: Weapon) -> WeaponTypeEntry:
        """Get the weapon type data of ``weapon``."""
        return self.get_data_by_id(weapon.value)


class WeaponTypeParser(MasterParserBase[WeaponTypeEntry]):
    """Class to parse the weapon type file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, WeaponTypeEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: WeaponTypeEntry.parse_raw(value) for key, value in entries.items()}
