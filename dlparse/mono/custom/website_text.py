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

    # pylint: disable=too-few-public-methods

    def __init__(self, lang_codes: Union[list[str], dict[str, str]], asset_dir: str):
        super().__init__(WebsiteTextParser, lang_codes, asset_dir, "WebsiteText")


class WebsiteTextParser(CustomParserBase):
    """Class to parse the website text asset file."""

    key_id: str = "id"

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[str, WebsiteTextEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: WebsiteTextEntry.parse_raw(value) for key, value in entries.items()}
