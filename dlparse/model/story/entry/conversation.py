"""Class for story entry representing a single converstation."""
from dataclasses import dataclass

from .base import StoryEntryBase

__all__ = ("StoryEntryConversation", "SPEAKER_NAME_SYS")

SPEAKER_NAME_SYS = "SYS"


@dataclass
class StoryEntryConversation(StoryEntryBase):
    """A single story conversation."""

    speaker_name: str
    conversation: str

    @property
    def is_speaker_system(self) -> bool:
        """Check if the speaker is system. If so, the conversation will be displayed like a system message."""
        return self.speaker_name == "SYS"

    def __repr__(self) -> str:
        return f"{self.speaker_name}:\n{self.conversation}"
