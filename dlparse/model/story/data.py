"""Story data model class."""
from dataclasses import InitVar, dataclass, field

from dlparse.enums import Language
from dlparse.mono.asset import StoryData
from dlparse.mono.custom import WebsiteTextAsset
from .entry import StoryEntryBase
from .parse import parse_story_commands_to_entries

__all__ = ("StoryModel",)


@dataclass
class StoryModel:
    """A story data model."""

    lang: Language
    story_data: StoryData

    text_asset: InitVar[WebsiteTextAsset]

    entries: list[StoryEntryBase] = field(init=False)

    def __post_init__(self, text_asset: WebsiteTextAsset) -> None:
        self.entries = parse_story_commands_to_entries(self.story_data, text_asset=text_asset)

    def __str__(self) -> str:
        story_content = "\n\n".join([f"#{idx: 3}: {repr(entry)}" for idx, entry in enumerate(self.entries, start=1)])
        return f"{self.story_data.title}\n\n{story_content}"
