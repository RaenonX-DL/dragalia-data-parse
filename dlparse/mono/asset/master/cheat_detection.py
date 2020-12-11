"""Classes for handling the cheat detection param asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("CheatDetectionEntry", "CheatDetectionAsset", "CheatDetectionParser")


@dataclass
class CheatDetectionEntry(MasterEntryBase):
    """Single entry of a cheat detection data."""

    max_enemy_damage: int
    max_enemy_break_damage: int
    max_enemy_player_distance: int
    max_player_heal: int
    max_player_move_speed: int

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "CheatDetectionEntry":
        return CheatDetectionEntry(
            id=data["_Id"],
            max_enemy_damage=data["_MaxEnemyDamage"],
            max_enemy_break_damage=data["_MaxEnemyBreakDamage"],
            max_enemy_player_distance=data["_MaxEnemyPlayerDistance"],
            max_player_heal=data["_MaxPlayerHeal"],
            max_player_move_speed=data["_MaxPlayerMoveSpeed"]
        )


class CheatDetectionAsset(MasterAssetBase[CheatDetectionEntry]):
    """Cheat detection parameter asset class."""

    asset_file_name = "CheatDetectionParam.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(CheatDetectionParser, file_location, asset_dir=asset_dir, file_like=file_like)


class CheatDetectionParser(MasterParserBase[CheatDetectionEntry]):
    """Class to parse the cheat detection parameter file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, CheatDetectionEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: CheatDetectionEntry.parse_raw(value) for key, value in entries.items()}
