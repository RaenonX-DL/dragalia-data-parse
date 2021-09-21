"""Class for story entry representing a single converstation."""
from dataclasses import InitVar, dataclass
from typing import Optional

from dlparse.enums import Language
from dlparse.mono.custom import WebsiteTextAsset
from .base import StoryEntryBase
from .const import PLAYER_NAME_TEXT_LABEL

__all__ = ("StoryEntryConversation", "SPEAKER_NAME_SYS")

SPEAKER_NAME_SYS = "SYS"


@dataclass
class StoryEntryConversation(StoryEntryBase):
    """A single story conversation."""

    speaker_name: str
    speaker_image_name: Optional[str]
    conversation: str

    text_asset: InitVar[WebsiteTextAsset]
    lang: InitVar[Language]

    def __post_init__(self, text_asset: WebsiteTextAsset, lang: Language):
        # Replace `{player_name}` placeholder
        player_name = text_asset.get_text(lang, PLAYER_NAME_TEXT_LABEL)
        self.speaker_name = self.speaker_name.replace("{player_name}", player_name)
        self.conversation = self.conversation.replace("{player_name}", player_name)

    @property
    def is_speaker_system(self) -> bool:
        """Check if the speaker is system. If so, the conversation will be displayed like a system message."""
        return self.speaker_name == "SYS"

    def __repr__(self) -> str:
        return f"{self.speaker_name} ({self.speaker_image_name}):\n{self.conversation}"
