"""Implementations to parse the story data into its corresponding model."""
from collections import defaultdict

from dlparse.enums import Language
from dlparse.mono.asset.story import StoryCommandPrintText, StoryCommandThemeSwitch, StoryData, has_story_content
from .entry import StoryEntryBase, StoryEntryBreak, StoryEntryConversation

__all__ = ("parse_story_commands_to_entries",)


def parse_story_commands_to_entries(story_data: StoryData) -> list[StoryEntryBase]:
    """Parse the commands in ``story_data`` into a list of story entry models."""
    # Group and sort the commands by its row
    commands_by_row = defaultdict(list)
    for command in story_data.data:
        commands_by_row[command.row].append(command)
    commands_sorted = [commands for _, commands in sorted(commands_by_row.items(), key=lambda item: item[0])]

    # Parse the story commands in the same row into entry model
    entries: list[StoryEntryBase] = []
    for command_same_row in commands_sorted:
        speaker = ""
        text = ""

        # Handle conversation pause in the same row
        is_in_conversation = False

        # Check each command in the same row according to its order defined in the data
        for command in command_same_row:
            if isinstance(command, StoryCommandThemeSwitch):
                # Command is a theme switch - consider it as a thematic break
                entries.append(StoryEntryBreak())
                break

            if isinstance(command, StoryCommandPrintText) and not is_in_conversation:
                is_in_conversation = True  # Using `print` command, getting back into conversation

                if not speaker:
                    if story_data.lang == Language.JP:
                        # For some reason, only JP is using this name mapping
                        speaker = story_data.name_asset.get_unit_jp_name(
                            command.speaker, on_not_found=command.speaker
                        )
                    else:
                        speaker = command.speaker

                if len(command.args) == 1 and story_data.name_asset.get_unit_jp_name(command.speaker, on_not_found=""):
                    # Speaker from command validated to be a speaker, this only occurs in JP story
                    continue

            if has_story_content(command):
                # Command has some story content
                text += command.content
                continue

            is_in_conversation = False

        if text:
            # `text` may be an empty string - story row is not a conversation
            entries.append(StoryEntryConversation(speaker, text))

    return entries
