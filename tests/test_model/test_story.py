from dlparse.enums import Language, UnitType
from dlparse.model import StoryEntryConversation
from dlparse.model.story.parse import parse_story_commands_to_entries
from dlparse.mono.manager import AssetManager


def test_jp_story_speaker_init_with_conversation(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100015081)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[0]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.conversation == "その人は、今まで見た誰よりも美しく輝いていて……。"


def test_jp_story_speaker_init_without_conversation(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100015081)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[3]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.conversation == "暑い……暑いですにゃ～！は、早く海に……。"


def test_jp_story_speaker_same_row_pause(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100015081)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[13]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.conversation == "ふふっ、素直な子は好きでしてよ。ほら、ケットシー。謝罪を。"


def test_jp_story_speaker_system_message(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100015081)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[38]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.conversation == "数日後"


def test_jp_story_speaker_name_in_conversation(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100015081)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[42]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.conversation == "この前出した手紙の返事、ですわね。これが何か？"


def test_jp_story_speaker_icon_follow(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100015081)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[7]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_image_path == "story/dragon/200013_01.png"


def test_jp_story_speaker_icon_offset(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100015081)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[8]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_image_path is None


def test_cht_story_speaker_init_with_conversation(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.CHT, UnitType.CHARACTER, 100015081)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[0]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.conversation == "那個人，比以前見過的任何人都要美麗且耀眼……"


def test_cht_story_speaker_init_without_conversation(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.CHT, UnitType.CHARACTER, 100015081)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[3]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.conversation == "好熱……好熱呀喵～！快、快點去海邊……"


def test_cht_story_speaker_same_row_pause(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_data = asset_manager.loader_story.load_unit_story(Language.CHT, UnitType.CHARACTER, 100015081)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[13]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.conversation == "呵呵，我很喜歡坦率的孩子喲。好了，凱特西。還不賠罪。"


def test_stories_have_same_lines_across_locale(asset_manager: AssetManager):
    # Summer Chelle Unit Story Ep. 1
    story_cht = parse_story_commands_to_entries(
        asset_manager.loader_story.load_unit_story(Language.CHT, UnitType.CHARACTER, 100015081),
        text_asset=asset_manager.asset_text_website
    )
    story_en = parse_story_commands_to_entries(
        asset_manager.loader_story.load_unit_story(Language.EN, UnitType.CHARACTER, 100015081),
        text_asset=asset_manager.asset_text_website
    )
    story_jp = parse_story_commands_to_entries(
        asset_manager.loader_story.load_unit_story(Language.JP, UnitType.CHARACTER, 100015081),
        text_asset=asset_manager.asset_text_website
    )

    assert len(story_cht) == len(story_jp) == len(story_en)


def test_story_speaker_player_name_replaced(asset_manager: AssetManager):
    story_data = asset_manager.loader_story.load_unit_story(Language.EN, UnitType.CHARACTER, 110030011)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[38]
    assert isinstance(entry, StoryEntryConversation)
    assert entry.speaker_name == "Euden"


def test_story_conversation_player_name_replaced(asset_manager: AssetManager):
    story_data = asset_manager.loader_story.load_unit_story(Language.EN, UnitType.CHARACTER, 100010041)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[28]
    assert isinstance(entry, StoryEntryConversation)
    assert "Euden" in entry.conversation
    assert "{player_name}" not in entry.conversation


def test_newline_replacement_in_en_story(asset_manager: AssetManager):
    story_data = asset_manager.loader_story.load_unit_story(Language.EN, UnitType.CHARACTER, 110335015)
    story_entries = parse_story_commands_to_entries(story_data, asset_manager.asset_text_website)

    entry = story_entries[6]
    assert isinstance(entry, StoryEntryConversation)
    assert "unable to" in entry.conversation
    assert "unableto" not in entry.conversation
