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
    speaker_image_path: Optional[str]
    conversation: str

    audio_paths: list[str]

    text_asset: InitVar[WebsiteTextAsset]
    lang: InitVar[Language]

    def _init_replace_player_name_placeholder(self, text_asset: WebsiteTextAsset, lang: Language) -> None:
        # Replace `{player_name}` placeholder
        player_name = text_asset.get_text(lang, PLAYER_NAME_TEXT_LABEL)
        self.speaker_name = self.speaker_name.replace("{player_name}", player_name)
        self.conversation = self.conversation.replace("{player_name}", player_name)

    def _init_replace_newline(self, lang: Language):
        # For EN, replace with a space; otherwise, replace with an empty string
        self.conversation = self.conversation.replace("\\n", " " if lang == Language.EN else "")

    def __post_init__(self, text_asset: WebsiteTextAsset, lang: Language) -> None:
        self._init_replace_player_name_placeholder(text_asset, lang)
        self._init_replace_newline(lang)

    @property
    def is_speaker_system(self) -> bool:
        """Check if the speaker is system. If so, the conversation will be displayed like a system message."""
        return self.speaker_name == "SYS"

    def __repr__(self) -> str:
        return f"{self.speaker_name} ({self.speaker_image_path}) - {' / '.join(self.audio_paths)}:\n" \
               f"{self.conversation}"
