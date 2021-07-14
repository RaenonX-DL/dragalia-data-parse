"""Functions to export simplified unit info."""
from dlparse.errors import (
    AbilityConditionUnconvertibleError, AbilityLimitDataNotFoundError, AbilityOnSkillUnconvertibleError,
    AbilityVariantUnconvertibleError,
)
from dlparse.export.entry import SimpleUnitInfoEntry
from dlparse.mono.manager import AssetManager

from .base import export_as_json, print_skipped_messages

__all__ = ("export_simple_info_as_entry_dict", "export_simple_info_as_json")


def export_simple_info_as_entry_dict(
        asset_manager: AssetManager, /, skip_unparsable: bool = True
) -> dict[int, SimpleUnitInfoEntry]:
    """Export all simplified unit info as an entry dict."""
    entry_dict: dict[int, SimpleUnitInfoEntry] = {}
    skipped_messages: list[str] = []

    playable_data = asset_manager.asset_chara_data.playable_data + asset_manager.asset_dragon_data.playable_data

    for unit_data in playable_data:
        try:
            entry_dict[unit_data.id] = SimpleUnitInfoEntry(asset_manager=asset_manager, unit_data=unit_data)
        except (AbilityOnSkillUnconvertibleError, AbilityConditionUnconvertibleError,
                AbilityVariantUnconvertibleError, AbilityLimitDataNotFoundError) as ex:
            if skip_unparsable:
                skipped_messages.append(
                    f"[Simple Info] Unit ID #{unit_data.id} "
                    f"({unit_data.get_name(asset_manager.asset_text_multi)})"
                )
                continue

            raise ex

    print_skipped_messages(skipped_messages)

    return entry_dict


def export_simple_info_as_json(file_path: str, asset_manager: AssetManager, /, skip_unparsable: bool = True):
    """Export all simplified unit info as json."""
    export_as_json(export_simple_info_as_entry_dict(asset_manager, skip_unparsable=skip_unparsable), file_path)
