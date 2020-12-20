"""Classes for handling the custom website text asset."""
import os
from dataclasses import dataclass
from typing import TextIO, Union

from dlparse.mono.asset.base import AssetBase, CustomParserBase, MasterEntryBase

__all__ = ("WebsiteTextEntry", "WebsiteTextAsset", "WebsiteTextParser")


@dataclass
class WebsiteTextEntry(MasterEntryBase):
    """Single entry of a website text data."""

    text: str

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "WebsiteTextEntry":
        return WebsiteTextEntry(
            id=data["id"],
            text=data["text"]
        )


class WebsiteTextAsset:
    """Website text asset class."""

    # pylint: disable=too-few-public-methods

    def __init__(self, lang_codes: list[str], asset_dir: str):
        self._assets: dict[str, dict[str, WebsiteTextEntry]] = {}

        for lang_code in lang_codes:
            file_path = os.path.join(asset_dir, f"WebsiteText@{lang_code}.json")
            file_like = AssetBase.get_file_like(file_path)

            self._assets[lang_code] = WebsiteTextParser.parse_file(file_like)

    def get_text(self, lang_code: str, label: str) -> str:
        """Get the text labeled as ``label`` in ``lang_code``."""
        return self._assets[lang_code][label].text


class WebsiteTextParser(CustomParserBase):
    """Class to parse the website text asset file."""

    key_id: str = "id"

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[str, WebsiteTextEntry]:
        entries = cls.get_entries_dict(file_like)

        return {key: WebsiteTextEntry.parse_raw(value) for key, value in entries.items()}
