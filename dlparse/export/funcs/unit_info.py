"""Functions to export unit info, including characters and dragons."""
from dlparse.errors import (
    AbilityConditionUnconvertibleError, AbilityLimitDataNotFoundError, AbilityOnSkillUnconvertibleError,
    AbilityVariantUnconvertibleError,
)
from dlparse.export.entry import CharaInfoEntry, DragonInfoEntry
from dlparse.mono.manager import AssetManager
from .base import export_as_json, print_skipped_messages

__all__ = (
    "export_chara_info_as_entries", "export_chara_info_as_json",
    "export_dragon_info_as_entries", "export_dragon_info_as_json",
)


def export_chara_info_as_entries(
        asset_manager: AssetManager, /, skip_unparsable: bool = True
) -> list[CharaInfoEntry]:
    """Export all character info as entries."""
    entries: list[CharaInfoEntry] = []
    skipped_messages: list[str] = []

    for chara_data in asset_manager.asset_chara_data.playable_data:
        try:
            entries.append(CharaInfoEntry(
                asset_manager=asset_manager, unit_data=chara_data
            ))
        except (AbilityOnSkillUnconvertibleError, AbilityConditionUnconvertibleError,
                AbilityVariantUnconvertibleError, AbilityLimitDataNotFoundError) as ex:
            if skip_unparsable:
                skipped_messages.append(
                    f"[Chara Info] Character ID #{chara_data.id} "
                    f"({chara_data.get_name(asset_manager.asset_text_multi)})"
                )
                continue

            raise ex

    print_skipped_messages(skipped_messages)

    return entries


def export_chara_info_as_json(file_path: str, asset_manager: AssetManager, /, skip_unparsable: bool = True):
    """Export all character info as json."""
    export_as_json(export_chara_info_as_entries(asset_manager, skip_unparsable=skip_unparsable), file_path)


def export_dragon_info_as_entries(
        asset_manager: AssetManager, /, skip_unparsable: bool = True
) -> list[DragonInfoEntry]:
    """Export all character info as entries."""
    entries: list[DragonInfoEntry] = []
    skipped_messages: list[str] = []

    for dragon_data in asset_manager.asset_dragon_data.playable_data:
        try:
            entries.append(DragonInfoEntry(
                asset_manager=asset_manager, unit_data=dragon_data
            ))
        except (AbilityOnSkillUnconvertibleError, AbilityConditionUnconvertibleError,
                AbilityVariantUnconvertibleError, AbilityLimitDataNotFoundError) as ex:
            if skip_unparsable:
                skipped_messages.append(
                    f"[Dragon Info] Dragon ID #{dragon_data.id} "
                    f"({dragon_data.get_name(asset_manager.asset_text_multi)})"
                )
                continue

            raise ex

    print_skipped_messages(skipped_messages)

    return entries


def export_dragon_info_as_json(file_path: str, asset_manager: AssetManager, /, skip_unparsable: bool = True):
    """Export all character info as json."""
    export_as_json(export_dragon_info_as_entries(asset_manager, skip_unparsable=skip_unparsable), file_path)
