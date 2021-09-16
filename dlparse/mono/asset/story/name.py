"""Implementations for managing the story code names."""
import json
from typing import Iterator, Optional, TextIO

from dlparse.mono.asset.base import AssetBase, ParserBase

__all__ = ("StoryNameAsset",)

StoryNameMapping = dict[str, str]


class StoryNameAsset(AssetBase[StoryNameMapping, tuple[str, str]]):
    """
    Contains the code name mapping of the speaker of a story conversation.

    This is only used in JP story. CH/EN stories are not using this mechanism to map their names.
    Instead, it's encoded in the story commands.
    """

    asset_file_name = "function_namelist_notedit.json"

    def __init__(self, story_dir: str) -> None:
        super().__init__(StoryNameParser, asset_dir=story_dir)

    def __iter__(self) -> Iterator[tuple[str, str]]:
        # False-negative
        # noinspection PyTypeChecker
        return iter(self.data.items())

    def get_unit_jp_name(self, code_name: str) -> Optional[str]:
        """Get the unit name in JP by its code name in story data."""
        return self.data.get(code_name)


class StoryNameParser(ParserBase[StoryNameMapping]):
    """Parses the story name list asset."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def parse_file(file_like: TextIO) -> StoryNameMapping:
        data = json.load(file_like)
        data = data["functions"][0]["variables"]

        keys = data["entriesKey"]
        values = data["entriesValue"]

        return dict(zip(keys, values))
