from collections import defaultdict

import pytest

from dlparse.enums import Language
from dlparse.export import export_unit_story_as_entry_dict
from dlparse.export.entry.story.conversation import StoryConversation
from dlparse.mono.manager import AssetManager


@pytest.skip
def test_exported_entries(asset_manager: AssetManager):
    entry_dict = export_unit_story_as_entry_dict(asset_manager, Language.CHT, skip_unparsable=False)

    assert len(entry_dict) > 0

    speaker_names_no_image = defaultdict(set)
    speaker_names_has_image = defaultdict(set)

    for stories in entry_dict.values():
        for story in stories:
            for entry in story.entries:
                if not isinstance(entry, StoryConversation):
                    continue

                if entry.base.speaker_image_path:
                    speaker_names_has_image[entry.base.speaker_name].add(entry.base.speaker_image_path)
                else:
                    speaker_names_no_image[entry.base.speaker_name].add(story.story_id)

    message = ""

    speaker_names_missing_image = set(speaker_names_has_image.keys()).intersection(speaker_names_no_image.keys())

    if speaker_names_missing_image:
        message = f"There are speakers missing icon ({len(speaker_names_missing_image)}):\n"
        message += "\n".join(
            f"- {name}\n"
            f"    Possible image paths {speaker_names_has_image[name]}\n"
            f"    Story IDs missing: {speaker_names_no_image[name]}"
            for name in speaker_names_missing_image
        )

    pytest.fail(message)
