"""Classes for handling the player action hit attribute asset."""
from dataclasses import dataclass
from typing import Union, Optional

from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("HitAttrEntry", "HitAttrAsset", "HitAttrParser")


@dataclass
class HitAttrEntry(MasterEntryBase):
    """Single entry of a hit attribute data."""

    id: str

    damage_modifier: float

    @staticmethod
    def parse_raw(data: dict[str, Union[str, float, int]]) -> "HitAttrEntry":
        return HitAttrEntry(
            id=data["_Id"],
            damage_modifier=data["_DamageAdjustment"],
        )

    @property
    def deal_damage(self) -> bool:
        """
        Check if the hit actually deals damage.

        Some hits seem to be dummy hit. For example, Renee S1 def down (`DAG_002_03_H03_DEFDOWN_LV03`).
        """
        return self.damage_modifier != 0


class HitAttrAsset(MasterAssetBase):
    """Player action hit attribute asset class."""

    asset_file_name = "PlayerActionhitAttribute.json"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(HitAttrParser, file_path, asset_dir=asset_dir)

    @staticmethod
    def get_hit_label(original_label: str, level: int) -> str:
        """
        Get the hit label at ``level``.

        For example, if ``original_label`` is ``SWD_110_04_H01_LV02`` and ``level`` is ``3``,
        the return will be ``SWD_110_04_H01_LV03``.
        """
        return original_label[:-1] + str(level)


class HitAttrParser(MasterParserBase):
    """Class to parse the player action hit attribute file."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, HitAttrEntry]:
        entries = cls.get_entries(file_path)

        return {key: HitAttrEntry.parse_raw(value) for key, value in entries.items()}
