"""Class representing """
import json
from typing import Optional, TextIO, TypeVar

from dlparse.mono.asset.base import AssetBase, ParserBase
from .command import StoryCommandBase, StoryCommandParser

__all__ = ("StoryData",)

T = TypeVar("T", bound=StoryCommandBase)


class StoryData(AssetBase[list[T]]):
    """A class containing a story."""

    def __iter__(self) -> list[T]:
        return self.data

    def __init__(self, file_location: Optional[str] = None):
        super().__init__(StoryDataParser, file_location)


class StoryDataParser(ParserBase[list[T]]):
    @staticmethod
    def parse_file(file_like: TextIO) -> list[T]:
        data = json.load(file_like)
        raw_commands = data["functions"][0]["commandList"]

        return [StoryCommandParser.parse_raw_command(raw_command) for raw_command in raw_commands]
