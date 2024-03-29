"""Functions to export the EX (Co-ab) and chained EX (CCA) data."""
from dlparse.errors import (
    AbilityConditionUnconvertibleError, AbilityLimitDataNotFoundError, AbilityOnSkillUnconvertibleError,
    AbilityVariantUnconvertibleError,
)
from dlparse.export.entry import CharaExAbiltiesEntry
from dlparse.mono.manager import AssetManager
from .base import export_as_json, print_skipped_messages

__all__ = ("export_ex_abilities_as_entries", "export_ex_abilities_as_json")


def export_ex_abilities_as_entries(
        asset_manager: AssetManager, /, skip_unparsable: bool = True
) -> list[CharaExAbiltiesEntry]:
    """Export EX and Chained EX abilities of each character as entries."""
    entries: list[CharaExAbiltiesEntry] = []
    skipped_messages: list[str] = []

    for chara_data in asset_manager.asset_chara_data.playable_data:
        try:
            entries.append(CharaExAbiltiesEntry(asset_manager=asset_manager, unit_data=chara_data))
        except (AbilityOnSkillUnconvertibleError, AbilityConditionUnconvertibleError,
                AbilityVariantUnconvertibleError, AbilityLimitDataNotFoundError) as ex:
            if skip_unparsable:
                skipped_messages.append(
                    f"[EX Ability] EX ID #{chara_data.ex_id_at_max_level} CEX ID #{chara_data.cex_id_at_max_level}) "
                    f"of {chara_data.get_name(asset_manager.asset_text_multi)} ({chara_data.id}): {ex}"
                )
                continue

            raise ex

    print_skipped_messages(skipped_messages)

    return entries


def export_ex_abilities_as_json(file_path: str, asset_manager: AssetManager, /, skip_unparsable: bool = True):
    """Export EX and Chained EX abilities of each character as json."""
    export_as_json(export_ex_abilities_as_entries(asset_manager, skip_unparsable=skip_unparsable), file_path)
