"""Function to export the skill identifiers."""
from typing import TYPE_CHECKING

from dlparse.export.entry import SkillIdentifierEntry, TextEntry
from .base import export_as_json
from .skill_atk import export_atk_skills_as_entries

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("export_skill_identifiers_as_json", "export_skill_identifiers_as_entry_dict")


def export_skill_identifiers_as_entry_dict(asset_manager: "AssetManager") -> dict[str, dict]:
    """Export the skill identifiers as an entry dict."""
    # Get all possible skill identifiers
    skill_identifiers: set[str] = set()
    for entry in export_atk_skills_as_entries(asset_manager):
        skill_identifiers.update(entry.skill_identifiers)

    # Obtain skill identifier entries
    return {
        skill_identifier: SkillIdentifierEntry(
            skill_identifier,
            TextEntry(
                asset_text_base=asset_manager.asset_text_website, labels=f"SKILL_IDENTIFIER_{skill_identifier}",
                asset_text_additional=asset_manager.asset_text_multi
            )
        ).to_json_entry()
        for skill_identifier in skill_identifiers
    }


def export_skill_identifiers_as_json(
        asset_manager: "AssetManager", file_path: str
):
    """Export the skill identifiers as a json file."""
    export_as_json(export_skill_identifiers_as_entry_dict(asset_manager), file_path)
