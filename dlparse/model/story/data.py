"""Story data model class."""
from dataclasses import dataclass, field

from dlparse.enums import Language
from dlparse.mono.asset import StoryData
from .entry import StoryEntryBase
from .parse import parse_story_commands_to_entries

__all__ = ("StoryModel",)


@dataclass
class StoryModel:
    """A story data model."""

    lang: Language
    story_data: StoryData

    entries: list[StoryEntryBase] = field(init=False)

    def __post_init__(self) -> None:
        self.entries = parse_story_commands_to_entries(self.story_data)

    def __repr__(self) -> str:
        return "\n\n".join([repr(entry) for entry in self.entries])
