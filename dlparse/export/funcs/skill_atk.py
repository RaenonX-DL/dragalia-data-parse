"""Functions to export the attacking skill data."""
from dlparse.export.entry import CharaAttackingSkillEntry
from dlparse.mono.asset import CharaDataEntry
from dlparse.mono.manager import AssetManager
from .base import export_as_json, export_skill_entries, export_transform_skill_entries

__all__ = ("export_atk_skill_as_json", "export_atk_skills_as_entries")


def export_atk_skills_of_chara(
        chara_data: CharaDataEntry, asset_manager: AssetManager, /,
        skip_unparsable: bool = True, include_dragon: bool = True
) -> tuple[list[CharaAttackingSkillEntry], list[str]]:
    """Export attacking skills of a character as entries."""
    ret: list[CharaAttackingSkillEntry] = []

    # Transform every skill entries
    skill_entries_data, skipped_messages = export_transform_skill_entries(
        asset_manager.transformer_skill.transform_attacking, chara_data, asset_manager,
        skip_unparsable=skip_unparsable, include_dragon=include_dragon
    )

    for id_entry, skill_data, skill_entries in skill_entries_data:
        for skill_entry in skill_entries:
            ret.append(CharaAttackingSkillEntry(
                asset_manager=asset_manager,
                chara_data=chara_data,
                condition_comp=skill_entry.condition_comp,
                skill_id_entry=id_entry,
                skill_data=skill_data.skill_data_raw,
                skill_data_to_parse=skill_entry,
            ))

    return ret, skipped_messages


def export_atk_skills_as_entries(
        asset_manager: AssetManager, /,
        skip_unparsable: bool = True, include_dragon: bool = True
) -> list[CharaAttackingSkillEntry]:
    """Export attacking skills of all characters to be a list of data entries ready to be exported."""
    return export_skill_entries(
        export_atk_skills_of_chara, asset_manager, skip_unparsable=skip_unparsable, include_dragon=include_dragon
    )


def export_atk_skill_as_json(
        file_path: str, /,
        asset_manager: AssetManager, skip_unparsable: bool = True, include_dragon: bool = True
):
    """Export the entries of the attacking skills as json."""
    entries = export_atk_skills_as_entries(
        asset_manager, skip_unparsable=skip_unparsable, include_dragon=include_dragon
    )

    export_as_json(entries, file_path)
