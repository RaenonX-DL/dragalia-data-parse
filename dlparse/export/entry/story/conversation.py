"""Implementations for story conversation entries."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, cast

from dlparse.model import StoryEntryBase, StoryEntryBreak, StoryEntryConversation
from ..base import JsonExportableEntryBase, JsonSchema

__all__ = ("StoryConversationEntryBase", "StoryConversationBreak", "StoryConversation")

T = TypeVar("T", bound=StoryEntryBase)


@dataclass
class StoryConversationEntryBase(Generic[T], JsonExportableEntryBase, ABC):
    """Story entry base class."""

    base: T

    @classmethod
    @abstractmethod
    def type_name(cls) -> str:
        """Type name of this story entry. This is used by the frontend to determine the entry type."""
        raise NotImplementedError()

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "type": str,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "type": self.type_name(),
        }


@dataclass
class StoryConversationBreak(StoryConversationEntryBase[StoryEntryBreak]):
    """Thematic break during a story conversation."""

    @classmethod
    def type_name(cls) -> str:
        return "break"


@dataclass
class StoryConversation(StoryConversationEntryBase[StoryEntryConversation]):
    """Single conversation."""

    @classmethod
    def type_name(cls) -> str:
        return "conversation"

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return cast(JsonSchema, super().json_schema) | {
            "speakerName": str,
            "speakerIcon": str,
            "isSys": bool,
            "content": str,
            "audioPaths": [str],
        }

    def to_json_entry(self) -> dict[str, Any]:
        return super().to_json_entry() | {
            "speakerName": self.base.speaker_name,
            "speakerIcon": self.base.speaker_image_path,
            "isSys": self.base.is_speaker_system,
            "content": self.base.conversation,
            "audioPaths": self.base.audio_paths,
        }
