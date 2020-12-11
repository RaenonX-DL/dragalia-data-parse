"""Classes for handling the text label asset."""
from dataclasses import dataclass
from typing import Optional, TextIO

from dlparse.errors import TextLabelNotFoundError
from dlparse.mono.asset.base import CustomParserBase, MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("TextEntry", "TextAsset", "MasterTextParser")


@dataclass
class TextEntry(MasterEntryBase):
    """Single entry of a text label."""

    text: str

    @staticmethod
    def parse_raw(data: dict[str, str]) -> "TextEntry":
        return TextEntry(
            id=data["_Id"],
            text=data["_Text"],
        )


class TextAsset(MasterAssetBase[TextEntry]):
    """
    Text label asset class.

    If custom asset is provided, entries in the original asset will be overwritten by the entries in the custom asset,
    if exist.
    """

    asset_file_name = "TextLabel.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None,
            custom_asset_dir: Optional[str] = None, custom_file_location: Optional[str] = None,
            custom_file_like: Optional[TextIO] = None,
    ):
        super().__init__(MasterTextParser, file_location, asset_dir=asset_dir, file_like=file_like)

        # Read in and overwrite the data by custom assets
        custom_file_path = self.get_file_path(
            file_location=custom_file_location, asset_dir=custom_asset_dir, on_fail=None
        )
        if custom_file_like or custom_file_path:
            self._data.update(CustomTextParser.parse_file(custom_file_like or self.get_file_like(custom_file_path)))

    def to_text(self, label: str, /, silent_fail: bool = True) -> str:
        """
        Convert ``label`` to its corresponding text.

        If ``silent_fail``, ``label`` will be the return if not found. Otherwise, raises :class:`ValueError`.

        :raises TextLabelNotFoundError: if silent fail is set to false, and the label is not found
        """
        text: TextEntry = self.get_data_by_id(label)

        if text:
            return text.text

        if silent_fail:
            return label

        raise TextLabelNotFoundError(label)


class MasterTextParser(MasterParserBase[TextEntry]):
    """Class to parse the master text label file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, TextEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: TextEntry.parse_raw(value) for key, value in entries.items()}


class CustomTextParser(CustomParserBase):
    """Class to parse the custom text label file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[int, TextEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: TextEntry.parse_raw(value) for key, value in entries.items()}
