"""Classes for handling the player action info asset."""
from dataclasses import dataclass
from typing import Union, Optional

from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("PlayerActionInfoEntry", "PlayerActionInfoAsset", "PlayerActionInfoParser")


@dataclass
class PlayerActionInfoEntry(MasterEntryBase):
    """Single entry of a player action info data."""

    is_dragon_attack: bool
    is_default_skill: bool
    is_fs_skill: bool
    is_unit_skill: bool

    heal_type: int  # DRAFT: could be an enum, may be used for recovery skill implementation

    max_bullet_count: int  # 0 = not applicable

    next_action_id: int
    casting_action_id: int
    is_next_action_shift_by_input: bool
    min_addl_input_count_for_next: int
    max_addl_input_count: int
    is_loop_action: bool

    is_ally_target: bool

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "PlayerActionInfoEntry":
        return PlayerActionInfoEntry(
            id=data["_Id"],
            is_dragon_attack=bool(data["_IsDragonAttack"]),
            is_default_skill=bool(data["_IsDefaultSkill"]),
            is_fs_skill=bool(data["_IsChargeSkill"]),
            is_unit_skill=bool(data["_IsHeroSkill"]),
            heal_type=data["_HealType"],
            max_bullet_count=data["_MaxStockBullet"],
            next_action_id=data["_NextAction"],
            casting_action_id=data["_CastingAction"],
            is_next_action_shift_by_input=bool(data["_IsNextActionShiftByInput"]),
            min_addl_input_count_for_next=data["_MinAdditionalInputNumForNextActionShift"],
            max_addl_input_count=data["_MaxAdditionalInput"],
            is_loop_action=bool(data["_IsLoopAction"]),
            is_ally_target=bool(data["_IsAllyTarget"]),
        )


class PlayerActionInfoAsset(MasterAssetBase[PlayerActionInfoEntry]):
    """Player action info asset class."""

    asset_file_name = "PlayerAction.json"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(PlayerActionInfoParser, file_path, asset_dir=asset_dir)


class PlayerActionInfoParser(MasterParserBase[PlayerActionInfoEntry]):
    """Class to parse the player action info file."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, PlayerActionInfoEntry]:
        entries = cls.get_entries(file_path)

        return {key: PlayerActionInfoEntry.parse_raw(value) for key, value in entries.items()}
