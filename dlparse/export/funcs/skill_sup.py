"""Functions to export the supportive skill data."""
from dlparse.export.entry import CharaSupportiveSkillEntry
from dlparse.mono.asset import CharaDataEntry
from dlparse.mono.manager import AssetManager
from .base import export_as_json, export_skill_entries, export_transform_skill_entries

__all__ = ("export_sup_skill_as_json", "export_sup_skills_as_entries")


def export_sup_skills_of_chara(
        chara_data: CharaDataEntry, asset_manager: AssetManager, /,
        skip_unparsable: bool = True, include_dragon: bool = False
) -> tuple[list[CharaSupportiveSkillEntry], list[str]]:
    """Export attacking skills of a character as entries."""
    ret: list[CharaSupportiveSkillEntry] = []

    # Transform every skill entries
    skill_entries_data, skipped_messages = export_transform_skill_entries(
        asset_manager.transformer_skill.transform_supportive, chara_data, asset_manager,
        skip_unparsable=skip_unparsable, include_dragon=include_dragon
    )

    for id_entry, skill_data, skill_entries in skill_entries_data:
        for skill_entry in skill_entries:
            for buff in skill_entry.max_lv_buffs:
                ret.append(CharaSupportiveSkillEntry(
                    asset_manager=asset_manager,
                    chara_data=chara_data,
                    condition_comp=skill_entry.condition_comp,
                    skill_data=skill_data.skill_data,
                    skill_id_entry=id_entry,
                    skill_data_to_parse=buff
                ))

    return ret, skipped_messages


def export_sup_skills_as_entries(
        asset_manager: AssetManager, /,
        skip_unparsable: bool = True, include_dragon: bool = False
) -> list[CharaSupportiveSkillEntry]:
    """Export attacking skills of all characters to be a list of data entries ready to be exported."""
    return export_skill_entries(
        export_sup_skills_of_chara, asset_manager, skip_unparsable=skip_unparsable, include_dragon=include_dragon
    )


def export_sup_skill_as_json(
        file_path: str, /,
        asset_manager: AssetManager, skip_unparsable: bool = True, include_dragon: bool = True
):
    """Export the entries of the attacking skills as json."""
    entries = export_sup_skills_as_entries(
        asset_manager, skip_unparsable=skip_unparsable, include_dragon=include_dragon
    )

    export_as_json(entries, file_path)
