"""Story command class for ``print``."""
from dataclasses import dataclass
from typing import Optional

from .base import StoryCommandBase

__all__ = ("StoryCommandPlaySound",)


@dataclass
class StoryCommandPlaySound(StoryCommandBase):
    """
    A story command that plays a sound.

    - 1st argument: voice file label
    """

    @property
    def label(self) -> str:
        """Audio file label."""
        return self.args[0]

    @property
    def is_voice(self) -> bool:
        """Return if the underlying audio label is a voice."""
        return self.label.startswith("VO")

    @property
    def path(self) -> Optional[str]:
        """
        Audio file network path rooted from the story audio directory in the audio depot.

        If the underlying label is not a voice (for example, SE or BGM), returns `None`.

        Root audio directory in the audio depot is:
        https://github.com/RaenonX-DL/dragalia-data-audio/tree/main/audio/localize/ja_jp/sound/v/story.
        """
        if not self.is_voice:
            return None

        audio_dir, _ = self.label.rsplit("_", 1)

        # This path must be a network path
        return f"{audio_dir.lower()}/{self.label}.wav"
