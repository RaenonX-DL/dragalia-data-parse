"""Classes for handling the custom website text asset."""
from dataclasses import dataclass
from typing import TextIO, Union

from dlparse.mono.asset.base import CustomParserBase, MasterEntryBase, MultilingualAssetBase, TextEntryBase

__all__ = ("WebsiteTextEntry", "WebsiteTextAsset", "WebsiteTextParser")


@dataclass
class WebsiteTextEntry(TextEntryBase, MasterEntryBase):
    """Single entry of a website text data."""

    text: str

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "WebsiteTextEntry":
        return WebsiteTextEntry(
            id=data["id"],
            text=data["text"]
        )


class WebsiteTextAsset(MultilingualAssetBase[WebsiteTextEntry]):
    """Website text asset class."""

    def __init__(self, lang_codes: Union[list[str], dict[str, str]], asset_dir: str):
        super().__init__(WebsiteTextParser, lang_codes, asset_dir, "WebsiteText")

    def get_all_ids(self, lang_code: str) -> list[str]:
        """Get all text entry IDs in ``lang_code``. If ``lang_code`` is unavailable, returns empty list."""
        if lang_code not in self._assets:
            return []

        return list(self._assets[lang_code].keys())


class WebsiteTextParser(CustomParserBase[WebsiteTextEntry]):
    """Class to parse the website text asset file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[str, WebsiteTextEntry]:
        entries = cls.get_entries_dict(file_like, key="id")

        return {key: WebsiteTextEntry.parse_raw(value) for key, value in entries.items()}
