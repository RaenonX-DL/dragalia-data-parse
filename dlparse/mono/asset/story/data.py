"""Class representing a story data entity."""
import json
from typing import Iterator, TextIO, TypeVar

from dlparse.enums import Language
from dlparse.mono.asset.base import AssetBase, ParserBase
from .command import StoryCommandBase
from .image import StoryImageAsset
from .name import StoryNameAsset
from .parse import parse_raw_command

__all__ = ("StoryData",)

T = TypeVar("T", bound=StoryCommandBase)


class StoryData(AssetBase[list[T], T]):
    """A class containing a story."""

    def __init__(
            self, file_location: str, lang: Language, name_asset: StoryNameAsset, image_asset: StoryImageAsset
    ) -> None:
        super().__init__(StoryDataParser, file_location)

        self._lang = lang
        self._name_asset = name_asset
        self._image_asset = image_asset

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    @property
    def lang(self) -> Language:
        """Get the language of this story data."""
        return self._lang

    @property
    def name_asset(self) -> StoryNameAsset:
        """Get the story name asset assigned when this is initialized."""
        return self._name_asset

    @property
    def image_asset(self) -> StoryImageAsset:
        """Get the story image asset assigned when this is initialized."""
        return self._image_asset


class StoryDataParser(ParserBase[list[T]]):
    """Class to parse story data."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def parse_file(file_like: TextIO) -> list[T]:
        data = json.load(file_like)
        raw_commands = data["functions"][0]["commandList"]

        return [parse_raw_command(raw_command) for raw_command in raw_commands]
