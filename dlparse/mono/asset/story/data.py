"""Class representing a story data entity."""
import json
from typing import Optional, TextIO, TypeVar

from dlparse.mono.asset.base import AssetBase, ParserBase
from .command import StoryCommandBase
from .parse import parse_raw_command

__all__ = ("StoryData",)

T = TypeVar("T", bound=StoryCommandBase)


class StoryData(AssetBase[list[T]]):
    """A class containing a story."""

    def __iter__(self) -> list[T]:
        return self.data

    # def print_text_contents_cht_en(self) -> None:
    #     for command in self.data:
    #         if isinstance(command, StoryCommandPrintText):
    #             print(f"{command.args[0]}:")
    #             print(command.content)
    #             print()
    #
    #         if isinstance(command, StoryCommandThemeSwitch):
    #             print("-------------")
    #             print()
    #
    # def print_text_contents_jp(self) -> None:
    #     commands_by_row: dict[int, list[T]] = defaultdict(list)
    #     for command in self.data:
    #         commands_by_row[command.row].append(command)
    #     grouped_commands = [commands for _, commands in sorted(commands_by_row.items(), key=lambda item: item[0])]
    #
    #     for command_same_row in grouped_commands:
    #         text = ""
    #
    #         for command in command_same_row:
    #             if isinstance(command, StoryCommandPrintText):
    #                 text += command.content
    #
    #             if isinstance(command, StoryCommandRuby):
    #                 text += command.content
    #
    #         if text:
    #             print(text)


class StoryDataParser(ParserBase[list[T]]):
    """Class to parse story data."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def parse_file(file_like: TextIO) -> list[T]:
        data = json.load(file_like)
        raw_commands = data["functions"][0]["commandList"]

        return [parse_raw_command(raw_command) for raw_command in raw_commands]
