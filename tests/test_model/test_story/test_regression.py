from dlparse.enums import Language, UnitType
from dlparse.model import StoryEntryConversation
from dlparse.model.story.parse import parse_story_commands_to_entries
from dlparse.mono.manager import AssetManager


def test_missing_speaker_icon_kamite_se(asset_manager: AssetManager):
    # OG!Chelle Unit Story Ep. 3
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100015043)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[0]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_image_path == "story/chara/120040_01.png"


def test_missing_speaker_icon_shimote_se(asset_manager: AssetManager):
    # Farren Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 110393011)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[2]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_image_path == "story/chara/100001_01.png"


def test_missing_speaker_icon_shimote_pos_d(asset_manager: AssetManager):
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100018075)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[2]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_image_path == "story/chara/110394_01.png"


def test_missing_speaker_icon_chara_set_pos_0(asset_manager: AssetManager):
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 110350011)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[4]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_image_path == "story/chara/110350_01.png"


def test_missing_speaker_icon_custom_patch(asset_manager: AssetManager):
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 110350011)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[5]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_image_path == "story/chara/110353_01.png"


def test_missing_speaker_icon_chara_set_3(asset_manager: AssetManager):
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 110379013)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[36]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_image_path == "story/chara/120038_01.png"


def test_audio_label_contained_in_text(asset_manager: AssetManager):
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 110011011)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[0]
    assert isinstance(entry, StoryEntryConversation)
    assert "VO_CHR" not in entry.conversation


def test_speaker_reveal_market(asset_manager: AssetManager):
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 110271011)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[1]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_name == "リナーシュ"
