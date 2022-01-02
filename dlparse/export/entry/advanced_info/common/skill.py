"""Classes for skill info in advanced unit info."""
from dataclasses import InitVar, dataclass, field
from typing import Any

from dlparse.mono.asset import SkillDataEntry, UnitEntry
from dlparse.mono.manager import AssetManager
from ...base import JsonExportableEntryBase, JsonSchema, TextEntry
from ...skill_atk import AttackingSkillEntry

__all__ = ("UnitSkillEntry",)


@dataclass
class OfficialSkillEntry(JsonExportableEntryBase):
    """An entry for a unit skill with official descriptions."""

    asset_manager: InitVar["AssetManager"]
    max_level: InitVar[int]
    skill_entry: InitVar[SkillDataEntry]

    icon_path: str = field(init=False)
    name: TextEntry = field(init=False)
    description: TextEntry = field(init=False)

    def __post_init__(self, asset_manager: AssetManager, max_level: int, skill_entry: SkillDataEntry):
        self.icon_path = skill_entry.get_icon_name_at_level(max_level)
        self.name = TextEntry(
            asset_text_base=asset_manager.asset_text_website,
            asset_text_additional=asset_manager.asset_text_multi,
            labels=skill_entry.name_label,
        )
        self.description = TextEntry(
            asset_text_base=asset_manager.asset_text_website,
            asset_text_additional=asset_manager.asset_text_multi,
            labels=skill_entry.get_description_label_at_level(max_level),
            # Skill for dragon ID 2980000XX doesn't have description because presumably it's for Kaleidoscope
            on_not_found="N/A"
        )

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "iconPath": str,
            "name": TextEntry.json_schema,
            "description": TextEntry.json_schema,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "iconPath": self.icon_path,
            "name": self.name.to_json_entry(),
            "description": self.description.to_json_entry()
        }


@dataclass
class UnitSkillEntry(JsonExportableEntryBase):
    """An entry that collects all skills of a unit."""

    asset_manager: InitVar["AssetManager"]
    unit_data: InitVar[UnitEntry]

    atk_skills: list[AttackingSkillEntry]

    official: list[OfficialSkillEntry] = field(init=False)

    def __post_init__(self, asset_manager: AssetManager, unit_data: UnitEntry):
        self.official = [
            OfficialSkillEntry(
                asset_manager, unit_data.max_skill_level(skill_id_entry.skill_num),
                asset_manager.asset_skill_data.get_data_by_id(skill_id_entry.skill_id)
            ) for skill_id_entry in unit_data.self_skill_id_entries
        ]

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "official": [OfficialSkillEntry.json_schema],
            "atkSkills": [AttackingSkillEntry.json_schema]
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "official": [official.to_json_entry() for official in self.official],
            "atkSkills": [atk_skill.to_json_entry() for atk_skill in self.atk_skills],
        }
