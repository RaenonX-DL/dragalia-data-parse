"""Implentations to parse story entry model into the conversation entries to be exported."""
from typing import Type, TypeVar

from dlparse.model import StoryEntryBase, StoryEntryBreak, StoryEntryConversation
from .conversation import StoryConversation, StoryConversationBreak, StoryConversationEntryBase

__all__ = ("parse_entry_to_conversations",)

T = TypeVar("T", bound=StoryEntryBase)
CT = TypeVar("CT", bound=StoryConversationEntryBase)

_class_mapping_conversation_entry: dict[Type[T], Type[CT]] = {
    StoryEntryBreak: StoryConversationBreak,
    StoryEntryConversation: StoryConversation,
}


def parse_entry_to_conversations(entries: list[T]) -> list[CT]:
    """Parses ``entries`` into a list of story conversation entries for exporting."""
    return [_class_mapping_conversation_entry[type(entry)](entry) for entry in entries]
