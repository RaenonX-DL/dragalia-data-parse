"""Functions to export story data."""
from typing import TYPE_CHECKING, cast

from dlparse.enums import Language
from dlparse.errors import StorySpeakerNameNotFoundError, StoryUnavailableError
from dlparse.export.entry import Story
from dlparse.model import StoryModel
from dlparse.utils import localize_path
from ..base import (
    UnitEntryParsingFunction, export_each_chara_entries, export_each_dragon_entries,
    export_to_dir,
)

if TYPE_CHECKING:
    from dlparse.mono.asset import UnitEntry, VariationIdentifier
    from dlparse.mono.manager import AssetManager

__all__ = ("export_unit_story_as_entry_dict", "export_unit_story_as_json")

_excludable_var_identifier: list["VariationIdentifier"] = [
    (100001, 1),  # OG Euden
    (110354, 1),  # Megaman
]


def export_story_of_lang(lang: Language) -> UnitEntryParsingFunction:
    """Gets the function that exports the story of an unit in ``lang``."""

    def export_story(
            unit_entry: "UnitEntry", asset_manager: "AssetManager",
            skip_unparsable: bool,
    ) -> tuple[list[Story], list[str]]:
        ret: list[Story] = []
        skipped_messages: list[str] = []

        unit_stories = asset_manager.asset_story_unit.get_data_by_variation_identifier(unit_entry.var_identifier)
        if not unit_stories:
            if unit_entry.var_identifier in _excludable_var_identifier:
                return ret, skipped_messages

            message = f"Story of unit: #{unit_entry.id} unavailable"
            if not skip_unparsable:
                raise StoryUnavailableError(message)

            skipped_messages.append(message)
            return ret, skipped_messages

        for unit_story in unit_stories:
            try:
                ret.append(Story(StoryModel(
                    lang, asset_manager.loader_story.load_unit_story(lang, unit_entry.unit_type, unit_story.id),
                    text_asset=asset_manager.asset_text_website
                )))
            except (StoryUnavailableError, StorySpeakerNameNotFoundError) as ex:
                if not skip_unparsable:
                    raise ex

                skipped_messages.append(f"Story of unit: #{unit_entry.id} story: #{unit_story.id} unparsable ({ex})")

        return ret, skipped_messages

    return export_story


def export_unit_story_as_entry_dict(
        asset_manager: "AssetManager", lang: Language, /,
        skip_unparsable: bool = True,
) -> dict[int, list[Story]]:
    """Export the stories of all characters and dragons."""
    ret: dict[int, list[Story]] = {}
    ret.update(export_each_chara_entries(export_story_of_lang(lang), asset_manager, skip_unparsable=skip_unparsable))
    ret.update(export_each_dragon_entries(export_story_of_lang(lang), asset_manager, skip_unparsable=skip_unparsable))
    return ret


def export_unit_story_as_json(file_dir: str, asset_manager: "AssetManager", /, skip_unparsable: bool = True) -> None:
    """Export the stories of all characters and dragons as json to ``file_dir``."""
    for lang in Language:
        entries = export_unit_story_as_entry_dict(
            asset_manager, cast(Language, lang), skip_unparsable=skip_unparsable
        )
        export_to_dir(entries, localize_path(file_dir, cast(Language, lang)))
