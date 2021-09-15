"""Class representing a story data entity."""
import json
from typing import TextIO, TypeVar

from dlparse.mono.asset.base import AssetBase, ParserBase
from .command import StoryCommandBase
from .parse import parse_raw_command

__all__ = ("StoryData",)

T = TypeVar("T", bound=StoryCommandBase)


class StoryData(AssetBase[list[T]]):
    """A class containing a story."""

    def __init__(self, file_location: str) -> None:
        super().__init__(StoryDataParser, file_location)

    def __iter__(self) -> list[T]:
        return self.data


class StoryDataParser(ParserBase[list[T]]):
    """Class to parse story data."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def parse_file(file_like: TextIO) -> list[T]:
        data = json.load(file_like)
        raw_commands = data["functions"][0]["commandList"]

        return [parse_raw_command(raw_command) for raw_command in raw_commands]
