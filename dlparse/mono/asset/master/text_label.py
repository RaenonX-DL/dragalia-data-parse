"""Classes for handling the text label asset."""
from dataclasses import dataclass
from typing import Optional

from dlparse.mono.asset.base import MasterEntryBase, MasterAssetBase, MasterParserBase

__all__ = ("TextEntry", "TextAsset", "TextParser")


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


class TextAsset(MasterAssetBase):
    """Text label asset class."""

    asset_file_name = "TextLabel.json"

    def __init__(self, file_path: Optional[str] = None, /,
                 asset_dir: Optional[str] = None):
        super().__init__(TextParser, file_path, asset_dir=asset_dir)

    def to_text(self, label: str, /, silent_fail: bool = True) -> str:
        """
        Convert ``label`` to its corresponding text.

        If ``silent_fail``, ``label`` will be the return if not found. Otherwise, raises :class:`ValueError`.

        :raises ValueError: if silent fail is set to false, and the label is not found
        """
        text: TextEntry = self.get_data_by_id(label)

        if text:
            return text.text

        if silent_fail:
            return label

        raise ValueError(f"Text of label `{label}` not found")


class TextParser(MasterParserBase):
    """Class to parse the text label file."""

    @classmethod
    def parse_file(cls, file_path: str) -> dict[int, TextEntry]:
        entries = cls.get_entries(file_path)

        return {key: TextEntry.parse_raw(value) for key, value in entries.items()}
