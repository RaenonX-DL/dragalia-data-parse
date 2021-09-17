"""Base class for story asset parser."""
import json
from typing import TextIO

from dlparse.mono.asset.base import ParserBase

__all__ = ("StoryAssetParser",)

StoryAssetDataMapping = dict[str, str]


class StoryAssetParser(ParserBase[StoryAssetDataMapping]):
    """Parses the story image mapping asset."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def parse_file(file_like: TextIO) -> StoryAssetDataMapping:
        data = json.load(file_like)
        data = data["functions"][0]["variables"]

        keys = data["entriesKey"]
        values = data["entriesValue"]

        return dict(zip(keys, values))
