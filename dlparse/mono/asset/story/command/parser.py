"""Class to parse a story command."""
from typing import Type, TypeVar

from dlparse.enums import StoryCommandType
from .base import RawCommand, StoryCommandBase
from .outline import StoryCommandOutline
from .text import StoryCommandPrintText
from .unknown import StoryCommandUnknown

__all__ = ("StoryCommandParser",)

T = TypeVar("T", bound=StoryCommandBase)


class StoryCommandParser:
    """Class to parse a story command into its corresponding class."""

    COMMAND_CLASS: dict[StoryCommandType, Type[StoryCommandBase]] = {
        StoryCommandType.UNKNOWN: StoryCommandUnknown,
        StoryCommandType.OUTLINE: StoryCommandOutline,
        StoryCommandType.PRINT: StoryCommandPrintText,
    }

    @classmethod
    def parse_raw_command(cls, raw_command: RawCommand) -> T:
        story_command_type = StoryCommandType(raw_command["command"])

        command_class: Type[T] = cls.COMMAND_CLASS[story_command_type]

        # False-negative as ``command_class`` is an instantiatable class
        # noinspection PyArgumentList
        return command_class(raw_command)
