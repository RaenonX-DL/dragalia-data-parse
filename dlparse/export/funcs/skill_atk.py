"""Functions to export the attacking skill data."""
from dlparse.export.entry import AttackingSkillEntry
from dlparse.mono.asset import UnitEntry
from dlparse.mono.manager import AssetManager

from .base import export_as_json, export_entries_merged, export_transform_skill_entries

__all__ = ("export_atk_skill_as_json", "export_atk_skills_as_entries")


def export_atk_skills(
        unit_data: UnitEntry, asset_manager: AssetManager, /,
        skip_unparsable: bool = True,
) -> tuple[list[AttackingSkillEntry], list[str]]:
    """Export attacking skills of a dragon as entries."""
    ret: list[AttackingSkillEntry] = []

    # Transform every skill entries
    skill_entries_data, skipped_messages = export_transform_skill_entries(
        asset_manager.transformer_skill.transform_attacking, unit_data, asset_manager,
        skip_unparsable=skip_unparsable,
    )

    for id_entry, skill_data, skill_entries in skill_entries_data:
        for skill_entry in skill_entries:
            ret.append(AttackingSkillEntry(
                asset_manager=asset_manager,
                unit_data=unit_data,
                condition_comp=skill_entry.condition_comp,
                skill_id_entry=id_entry,
                skill_data=skill_data.skill_data,
                skill_data_to_parse=skill_entry,
            ))

    return ret, skipped_messages


def export_atk_skills_as_entries(
        asset_manager: AssetManager, /,
        skip_unparsable: bool = True, include_dragon: bool = True
) -> list[AttackingSkillEntry]:
    """
    Export attacking skills of all characters to be a list of data entries ready to be exported.

    ``include_dragon`` indicates if the dragon skills should be included.
    """
    return export_entries_merged(
        export_atk_skills, asset_manager,
        skip_unparsable=skip_unparsable, include_dragon=include_dragon
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
