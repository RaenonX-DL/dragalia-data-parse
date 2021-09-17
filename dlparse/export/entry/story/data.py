"""Story data implementations used for exporting."""
from dataclasses import dataclass, field
from typing import Any

from dlparse.model import StoryModel
from .conversation import StoryConversationEntryBase
from .parse import parse_entry_to_conversations
from ..base import JsonExportableEntryBase, JsonSchema

__all__ = ("Story",)


@dataclass
class Story(JsonExportableEntryBase):
    """A single story data to be exported."""

    story_data: StoryModel

    entries: list[StoryConversationEntryBase] = field(init=False)

    def __post_init__(self) -> None:
        self.entries = parse_entry_to_conversations(self.story_data.entries)

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "conversations": [StoryConversationEntryBase],
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "conversations": [entry.to_json_entry() for entry in self.entries],
        }
