from dlparse.enums import Language, UnitType
from dlparse.model import StoryEntryConversation
from dlparse.model.story.parse import parse_story_commands_to_entries
from dlparse.mono.manager import AssetManager


def test_missing_speaker_icon(asset_manager: AssetManager):
    # OG!Chelle Unit Story Ep. 3
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100015043)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[0]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_image_path == "story/chara/120040_01.png"
