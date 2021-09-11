"""Classes for handling the unit story group asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase
from dlparse.mono.asset.extension import VariationIdentifier, VariedEntry

__all__ = ("UnitStoryGroupEntry", "UnitStoryGroupAsset")


@dataclass
class UnitStoryGroupEntry(VariedEntry, MasterEntryBase):
    """Single entry of a unit story group data."""

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "UnitStoryGroupEntry":
        return UnitStoryGroupEntry(
            id=data["_Id"],
            base_id=data["_BaseId"],
            variation_id=data["_VariationId"]
        )


class UnitStoryGroupAsset(MasterAssetBase[UnitStoryGroupEntry]):
    """Unit story group asset class."""

    asset_file_name = "UnitStoryGroup.json"

    def _init_lookup_by_var(self):
        self._lookup_by_var: dict[VariationIdentifier, UnitStoryGroupEntry] = {}
        for entry in self:
            self._lookup_by_var[entry.var_identifier] = entry

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(UnitStoryGroupParser, file_location, asset_dir=asset_dir, file_like=file_like)

        self._init_lookup_by_var()

    def get_data_by_variation_identifier(self, var_identifier: VariationIdentifier) -> Optional[UnitStoryGroupEntry]:
        return self._lookup_by_var.get(var_identifier)


class UnitStoryGroupParser(MasterParserBase[UnitStoryGroupEntry]):
    """Class to parse the unit story group file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, UnitStoryGroupEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: UnitStoryGroupEntry.parse_raw(value) for key, value in entries.items()}
