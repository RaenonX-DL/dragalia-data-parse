import pytest

from dlparse.enums import Language
from dlparse.export import export_unit_story_as_entry_dict
from dlparse.export.entry.story.conversation import StoryConversation
from dlparse.mono.manager import AssetManager


def test_story_conversation_no_voice_label(asset_manager: AssetManager):
    entry_dict = export_unit_story_as_entry_dict(asset_manager, Language.CHT, skip_unparsable=False)

    assert len(entry_dict) > 0

    for stories in entry_dict.values():
        for story in stories:
            for idx, entry in enumerate(story.entries):
                if not isinstance(entry, StoryConversation):
                    continue

                conversation = entry.base.conversation

                if "VO" not in conversation:
                    continue

                pytest.fail(
                    f"Conversation in Entry #{idx} of story ID #{story.story_id} "
                    f"contains voice label: {conversation}"
                )
