"""Implementations to parse a story command."""
from typing import Type, TypeVar

from dlparse.enums import StoryCommandType
from .command import RawCommand, StoryCommandBase, StoryCommandOutline, StoryCommandPrintText, StoryCommandUnknown

__all__ = ("parse_raw_command",)

T = TypeVar("T", bound=StoryCommandBase)

_command_class: dict[StoryCommandType, Type[StoryCommandBase]] = {
    StoryCommandType.UNKNOWN: StoryCommandUnknown,
    StoryCommandType.OUTLINE: StoryCommandOutline,
    StoryCommandType.PRINT: StoryCommandPrintText,
}


def parse_raw_command(raw_command: RawCommand) -> T:
    """Parses ``raw_command`` into its corresponding story command class."""
    story_command_type = StoryCommandType(raw_command["command"])

    command_class: Type[T] = _command_class[story_command_type]

    # False-negative as ``command_class`` is an instantiatable class
    # noinspection PyArgumentList
    return command_class(raw_command)
