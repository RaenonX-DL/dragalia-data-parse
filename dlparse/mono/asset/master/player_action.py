"""Classes for handling the player action info asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("PlayerActionInfoEntry", "PlayerActionInfoAsset")


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

    is_action_loop: bool
    is_action_counter: bool
    is_ally_target: bool

    @property
    def has_next_action_staged(self) -> bool:
        """
        If this action chooses the action to be used according to additional input count.

        Gala Thor uses this strategy to pick the action to be triggered.
        """
        return self.is_next_action_shift_by_input and self.next_action_id

    @property
    def has_next_action_looped(self) -> bool:
        """
        If this action loops the next action specific amount of times according to the additional input count.

        Lathna uses this strategy.
        """
        return bool(self.max_addl_input_count)

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
            is_action_loop=bool(data["_IsLoopAction"]),
            is_action_counter=bool(data["_IsCounterAction"]),
            is_ally_target=bool(data["_IsAllyTarget"]),
        )


class PlayerActionInfoAsset(MasterAssetBase[PlayerActionInfoEntry]):
    """Player action info asset class."""

    asset_file_name = "PlayerAction.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(PlayerActionInfoParser, file_location, asset_dir=asset_dir, file_like=file_like)

    def get_action_id_chain(self, parent_action_id: int) -> list[int]:
        """Get action ID chain starting from ``parent_action_id``."""
        action_id_chain = []

        while parent_action_id:
            action_id_chain.append(parent_action_id)
            action_data = self.get_data_by_id(parent_action_id)

            parent_action_id = action_data.next_action_id

        return action_id_chain


class PlayerActionInfoParser(MasterParserBase[PlayerActionInfoEntry]):
    """Class to parse the player action info file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, PlayerActionInfoEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: PlayerActionInfoEntry.parse_raw(value) for key, value in entries.items()}
