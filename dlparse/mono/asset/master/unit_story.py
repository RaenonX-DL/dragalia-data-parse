"""Classes for handling the unit story asset."""
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.mono.asset.base import GroupedStoryAssetBase, GroupedStoryEntryBase, MasterEntryBase, MasterParserBase
from dlparse.mono.asset.extension import VariationIdentifier, VariedEntry

__all__ = ("UnitStoryEntry", "UnitStoryAsset")


@dataclass
class UnitStoryEntry(VariedEntry, GroupedStoryEntryBase, MasterEntryBase):
    """Single entry of a unit story data."""

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "UnitStoryEntry":
        return UnitStoryEntry(
            id=data["_Id"],
            title_label=data["_Title"],
            group_id=data["_GroupId"],
            base_id=data["_BaseId"],
            variation_id=data["_VariationId"]
        )


class UnitStoryAsset(GroupedStoryAssetBase[UnitStoryEntry]):
    """Unit story asset class."""

    asset_file_name = "UnitStory.json"

    def _init_lookup_by_var(self):
        self._lookup_by_var: dict[VariationIdentifier, list[UnitStoryEntry]] = defaultdict(list)
        for entry in self.data.values():
            self._lookup_by_var[entry.var_identifier].append(entry)

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(UnitStoryParser, file_location, asset_dir=asset_dir, file_like=file_like)

        self._init_lookup_by_var()

    def get_data_by_variation_identifier(self, var_identifier: VariationIdentifier) -> Optional[list[UnitStoryEntry]]:
        """Get the story entries that has ``var_identifier`` as its variation identifier."""
        return self._lookup_by_var.get(var_identifier)


class UnitStoryParser(MasterParserBase[UnitStoryEntry]):
    """Class to parse the unit story file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, UnitStoryEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: UnitStoryEntry.parse_raw(value) for key, value in entries.items()}
