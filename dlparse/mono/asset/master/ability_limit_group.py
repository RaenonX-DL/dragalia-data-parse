"""Classes for handling the ability limit group data asset."""
from dataclasses import dataclass
from typing import Any, Optional, TextIO, Union

from dlparse.errors import AbilityLimitDataNotFoundError
from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("AbilityLimitGroupEntry", "AbilityLimitGroupAsset")

THROW_ERROR = object()


@dataclass
class AbilityLimitGroupEntry(MasterEntryBase):
    """Single entry of a cheat detection data."""

    max_value: float

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "AbilityLimitGroupEntry":
        return AbilityLimitGroupEntry(
            id=data["_Id"],
            max_value=data["_MaxLimitedValue"]
        )


class AbilityLimitGroupAsset(MasterAssetBase[AbilityLimitGroupEntry]):
    """Ability limit group asset class."""

    asset_file_name = "AbilityLimitedGroup.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(AbilityLimitGroupParser, file_location, asset_dir=asset_dir, file_like=file_like)

    def get_max_value(self, data_id: int, on_not_found: Any = THROW_ERROR) -> float:
        """
        Get the max value of ``data_id``.

        If ``on_not_found`` is given, then the given value will be returned if the data is not found.

        :raises AbilityLimitDataNotFoundError: if the ability limit data is not found and `on_not_found` is not given
        """
        if data := self.get_data_by_id(data_id):
            return data.max_value

        if on_not_found is THROW_ERROR:
            raise AbilityLimitDataNotFoundError(data_id)

        return on_not_found


class AbilityLimitGroupParser(MasterParserBase[AbilityLimitGroupEntry]):
    """Class to parse the ability limit group file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, AbilityLimitGroupEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: AbilityLimitGroupEntry.parse_raw(value) for key, value in entries.items()}
