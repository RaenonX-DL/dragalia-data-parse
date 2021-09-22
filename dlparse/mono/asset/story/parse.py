"""Implementations to parse a story command."""
from typing import Type, TypeVar, cast

from dlparse.enums import StoryCommandType
from .command import (
    RawCommand, StoryCommandAddBook, StoryCommandBase, StoryCommandHasContent, StoryCommandOutline,
    StoryCommandPlaySound, StoryCommandPrintText, StoryCommandRuby, StoryCommandSetChara, StoryCommandThemeSwitch,
    StoryCommandUnknown,
)

__all__ = ("parse_raw_command", "has_story_content")

T = TypeVar("T", bound=StoryCommandBase)

_command_class: dict[StoryCommandType, Type[StoryCommandBase]] = {
    StoryCommandType.UNKNOWN: StoryCommandUnknown,
    StoryCommandType.OUTLINE: StoryCommandOutline,
    StoryCommandType.PRINT: StoryCommandPrintText,
    StoryCommandType.RUBY: StoryCommandRuby,
    StoryCommandType.BLACK_OUT: StoryCommandThemeSwitch,
    StoryCommandType.WHITE_OUT: StoryCommandThemeSwitch,
    StoryCommandType.ADD_TEXT: StoryCommandAddBook,
    StoryCommandType.CHARA_SET: StoryCommandSetChara,
    StoryCommandType.CHARA_SET_0: StoryCommandSetChara,
    StoryCommandType.CHARA_KAMITE_SE: StoryCommandSetChara,
    StoryCommandType.CHARA_SHIMOTE_SE: StoryCommandSetChara,
    StoryCommandType.PLAY_SOUND: StoryCommandPlaySound,
}


def parse_raw_command(raw_command: RawCommand) -> T:
    """Parses ``raw_command`` into its corresponding story command class."""
    story_command_type = StoryCommandType(raw_command["command"])

    command_class: Type[T] = cast(Type[T], _command_class[story_command_type])

    # False-negative as ``command_class`` is an instantiatable class
    # noinspection PyArgumentList
    return command_class(raw_command)


def has_story_content(story_command: T) -> bool:
    """Check if ``story_command`` has some story content."""
    return isinstance(story_command, StoryCommandHasContent) and not isinstance(story_command, StoryCommandOutline)
