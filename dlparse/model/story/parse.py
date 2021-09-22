"""Implementations to parse the story data into its corresponding model."""
from collections import defaultdict
from typing import Optional

from dlparse.enums import Language
from dlparse.mono.asset import (
    StoryCommandHasContent, StoryCommandPlaySound, StoryCommandPrintText, StoryCommandSetChara,
    StoryCommandThemeSwitch, StoryData, has_story_content,
)
from dlparse.mono.custom import WebsiteTextAsset
from .entry import SPEAKER_NAME_SYS, StoryEntryBase, StoryEntryBreak, StoryEntryConversation

__all__ = ("parse_story_commands_to_entries",)


def get_speaker_from_command(story_data: StoryData, command: StoryCommandPrintText) -> str:
    """Get the story speaker of ``command``."""
    if story_data.lang == Language.JP:
        # For some reason, only JP is using this name mapping mechanism
        return story_data.name_asset.get_unit_jp_name(command.speaker, on_not_found=command.speaker)

    return command.speaker


def get_content_from_command(story_data: StoryData, command: StoryCommandHasContent) -> str:
    """
    Get the story content of ``command``.

    Returns empty string if the command does/should not have a content.
    """
    if (
            story_data.lang == Language.JP
            and story_data.name_asset.get_unit_jp_name(command.content, on_not_found="")
    ):
        # The command content is actually the speaker
        # For some reason, this only occurs in JP story
        return ""

    if command.content == SPEAKER_NAME_SYS:
        # Content is system message as speaker
        return ""

    return command.content


# Disabling `C901` because this functions can't be de-coupled (too many cross-row variables)
def parse_story_commands_to_entries(  # noqa: C901
        story_data: StoryData, /,
        text_asset: WebsiteTextAsset
) -> list[StoryEntryBase]:
    """Parse the commands in ``story_data`` into a list of story entry models."""
    # Group and sort the commands by its row
    commands_by_row = defaultdict(list)
    for command in story_data.data:
        commands_by_row[command.row].append(command)
    commands_sorted = [commands for _, commands in sorted(commands_by_row.items(), key=lambda item: item[0])]

    # Parse the story commands in the same row into entry model
    entries: list[StoryEntryBase] = []

    # Command for setting the image will be in the different row from the conversation# Command for setting the
    # image will be in the different row from the conversation
    speaker_image_code = None
    # This mapping helps fixing the image of a speaker to be the same
    speaker_image_code_dict: dict[str, Optional[str]] = {}

    audio_paths: list[str] = []

    for command_same_row in commands_sorted:
        speaker = ""
        text = ""

        # Check each command in the same row according to its order defined in the data
        for command in command_same_row:
            if isinstance(command, StoryCommandThemeSwitch):
                # Command is a theme switch - consider it as a thematic break
                entries.append(StoryEntryBreak())
                break

            if isinstance(command, StoryCommandSetChara) and not speaker_image_code:
                speaker_image_code = command.image_code
                continue

            if isinstance(command, StoryCommandPrintText) and not speaker:
                speaker = get_speaker_from_command(story_data, command)

            if isinstance(command, StoryCommandPlaySound) and (audio_path := command.path):
                audio_paths.append(audio_path)
                continue

            if has_story_content(command):
                text += get_content_from_command(story_data, command)

        if text:
            if speaker not in speaker_image_code_dict:
                speaker_image_code_dict[speaker] = speaker_image_code

            image_path = story_data.image_asset.get_image_path(speaker_image_code_dict.get(speaker))

            # `text` may be an empty string - story row is not a conversation
            entries.append(StoryEntryConversation(
                speaker, image_path, text, audio_paths, text_asset=text_asset, lang=story_data.lang
            ))
            speaker_image_code = None  # Reset speaker image code
            audio_paths = []  # Reset audio paths

    return entries
