"""Classes for handling the character mode data asset."""
from dataclasses import dataclass
from typing import Union, Optional

from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("CharaModeEntry", "CharaModeAsset", "CharaModeParser")


@dataclass
class CharaModeEntry(MasterEntryBase):
    """Single entry of a character mode data."""

    transmode_action_id: int

    skill_id_1: int
    skill_id_2: int

    text_label: str

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "CharaModeEntry":
        return CharaModeEntry(
            id=data["_Id"],
            transmode_action_id=data["_ActionId"],
            skill_id_1=data["_Skill1Id"],
            skill_id_2=data["_Skill2Id"],
            text_label=data["_Text"]
        )

    @property
    def skill_ids(self) -> list[int]:
        """Get a list of effective skill IDs."""
        return [skill_id for skill_id in (self.skill_id_1, self.skill_id_2) if skill_id != 0]


class CharaModeAsset(MasterAssetBase[CharaModeEntry]):
    """Character mode data asset class."""

    asset_file_name = "CharaModeData.json"

    def _init_fill_name_label(self):
        # Auto fill custom mode name text label

        for data in self:
            if not data.text_label:  # Only fill if no label exists
                data.text_label = f"CUSTOM_CHARA_MODE_{data.id:04}"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(CharaModeParser, file_path, asset_dir=asset_dir)

        self._init_fill_name_label()


class CharaModeParser(MasterParserBase[CharaModeEntry]):
    """Class to parse the character mode data file."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, CharaModeEntry]:
        entries = cls.get_entries(file_path)

        return {key: CharaModeEntry.parse_raw(value) for key, value in entries.items()}
