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

    story_model: StoryModel

    story_id: int = field(init=False)
    title: str = field(init=False)
    entries: list[StoryConversationEntryBase] = field(init=False)

    def __post_init__(self) -> None:
        story_data = self.story_model.story_data

        self.story_id = story_data.story_id
        self.title = story_data.title
        self.entries = parse_entry_to_conversations(self.story_model.entries)

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "id": int,
            "title": str,
            "conversations": [StoryConversationEntryBase],
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "id": self.story_id,
            "title": self.title,
            "conversations": [entry.to_json_entry() for entry in self.entries],
        }
