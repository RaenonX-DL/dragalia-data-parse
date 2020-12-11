"""Classes for handling the skill chain data asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.enums import SkillChainCondition
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("SkillChainEntry", "SkillChainAsset", "SkillChainParser")


@dataclass
class SkillChainEntry(MasterEntryBase):
    """Single entry of a single skill chain data."""

    group_id: int
    chain_condition: SkillChainCondition

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "SkillChainEntry":
        return SkillChainEntry(
            id=data["_Id"],
            group_id=data["_GroupId"],
            chain_condition=SkillChainCondition(data["_ActivateCondition"]),
        )


class SkillChainAsset(MasterAssetBase[SkillChainEntry]):
    """Skill chain data asset class."""

    asset_file_name = "SkillChainData.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(SkillChainParser, file_location, asset_dir=asset_dir, file_like=file_like)

    def get_data_by_group_id(self, group_id: int) -> list[SkillChainEntry]:
        """Get a list of skill chain data by its ``group_id``."""
        return self.filter(lambda entry: entry.group_id == group_id)


class SkillChainParser(MasterParserBase[SkillChainEntry]):
    """Class to parse the skill chain data file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, SkillChainEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: SkillChainEntry.parse_raw(value) for key, value in entries.items()}
