"""Classes for handling the action grant asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import AbilityTargetAction
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("ActionGrantEntry", "ActionGrantAsset")


@dataclass
class ActionGrantEntry(MasterEntryBase):
    """Single entry of an action grant data."""

    duration_sec: float  # 0 means infinite
    target_action: AbilityTargetAction
    action_condition_id: int

    @staticmethod
    def parse_raw(data: dict[str, Union[str, Union[float, int]]]) -> "ActionGrantEntry":
        return ActionGrantEntry(
            id=data["_Id"],
            duration_sec=data["_DurationSec"],
            target_action=AbilityTargetAction(data["_TargetAction"]),
            action_condition_id=data["_GrantCondition"]
        )


class ActionGrantAsset(MasterAssetBase[ActionGrantEntry]):
    """Action grant asset class."""

    asset_file_name = "ActionGrant.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(ActionGrantParser, file_location, asset_dir=asset_dir, file_like=file_like)


class ActionGrantParser(MasterParserBase[ActionGrantEntry]):
    """Class to parse the action grant asset file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, ActionGrantEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: ActionGrantEntry.parse_raw(value) for key, value in entries.items()}
