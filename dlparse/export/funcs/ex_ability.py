"""Functions to export the EX (Co-ab) and chained EX (CCA) data."""
from dlparse.errors import (
    AbilityConditionUnconvertibleError, AbilityLimitDataNotFoundError, AbilityOnSkillUnconvertibleError,
    AbilityVariantUnconvertibleError,
)
from dlparse.export.entry import CharaExAbiltiesEntry
from dlparse.mono.manager import AssetManager
from .base import export_as_json

__all__ = ("export_ex_abilities_as_entries", "export_ex_abilities_as_json")


def export_ex_abilities_as_entries(
        asset_manager: AssetManager, /, skip_unparsable: bool = True
) -> list[CharaExAbiltiesEntry]:
    """Export EX and Chained EX abilities of each character as entries."""
    entries: list[CharaExAbiltiesEntry] = []
    skipped_messages: list[str] = []

    for chara_data in asset_manager.asset_chara_data.playable_chara_data:
        ex_data = asset_manager.transformer_ability.transform_ex_ability(chara_data.ex_id_at_max_level)
        chained_ex_data = asset_manager.transformer_ability.transform_chained_ex_ability(
            chara_data.cex_id_at_max_level
        )

        try:
            entries.append(CharaExAbiltiesEntry(
                asset_manager=asset_manager, chara_data=chara_data,
                ex_ability_data=ex_data, cex_ability_data=chained_ex_data
            ))
        except (AbilityOnSkillUnconvertibleError, AbilityConditionUnconvertibleError,
                AbilityVariantUnconvertibleError, AbilityLimitDataNotFoundError) as ex:
            if skip_unparsable:
                skipped_messages.append(
                    f"[EX Ability] EX ID #{chara_data.ex_id_at_max_level} CEX ID #{chara_data.cex_id_at_max_level}) "
                    f"of {chara_data.get_chara_name(asset_manager.asset_text)} ({chara_data.id}): {ex}"
                )
                continue

            raise ex

    if skipped_messages:
        print()
        print(f"Some ({len(skipped_messages)}) items were skipped:")

        for msg in skipped_messages:
            print(msg)

    return entries


def export_ex_abilities_as_json(file_path: str, asset_manager: AssetManager, /, skip_unparsable: bool = True):
    """Export EX and Chained EX abilities of each character as json."""
    export_as_json(export_ex_abilities_as_entries(asset_manager, skip_unparsable=skip_unparsable), file_path)
