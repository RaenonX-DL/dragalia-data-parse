"""Function to export the skill identifiers."""
import json
import os
from typing import TYPE_CHECKING

from dlparse.export.entry import SkillIdentifierEntry, TextEntry
from .skill_atk import export_atk_skills_as_entries

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("export_skill_identifiers_as_json",)


def export_skill_identifiers_as_json(
        asset_manager: "AssetManager", file_path: str
):
    """Export the skill identifiers to be a json file."""
    # Get all possible skill identifiers
    skill_identifiers: set[str] = set()
    for entry in export_atk_skills_as_entries(asset_manager):
        skill_identifiers.update(entry.skill_identifiers)

    # Obtain its translations
    json_dict = {
        skill_identifier: SkillIdentifierEntry(
            skill_identifier,
            TextEntry(asset_manager.asset_text_website, f"SKILL_IDENTIFIER_{skill_identifier}")
        ).to_json_entry()
        for skill_identifier in skill_identifiers
    }

    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directory if needed
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_dict, f, ensure_ascii=False)
