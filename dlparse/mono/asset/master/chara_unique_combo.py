"""Classes for handling the character unique combo asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("CharaUniqueComboEntry", "CharaUniqueComboAsset")


@dataclass
class CharaUniqueComboEntry(MasterEntryBase):
    """Single entry of a character unique combo data."""

    action_id: int
    max_combo_count: int

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "CharaUniqueComboEntry":
        return CharaUniqueComboEntry(
            id=data["_Id"],
            action_id=data["_ActionId"],
            max_combo_count=data["_MaxComboNum"],
        )


class CharaUniqueComboAsset(MasterAssetBase[CharaUniqueComboEntry]):
    """Character unique combo asset class."""

    asset_file_name = "CharaUniqueCombo.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(CharaUniqueComboParser, file_location, asset_dir=asset_dir, file_like=file_like)


class CharaUniqueComboParser(MasterParserBase[CharaUniqueComboEntry]):
    """Class to parse the character unique combo file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, CharaUniqueComboEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: CharaUniqueComboEntry.parse_raw(value) for key, value in entries.items()}
