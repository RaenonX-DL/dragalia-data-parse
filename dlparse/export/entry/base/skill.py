"""Base classes for the skill data entries to be exported."""
from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import Any, Generic, TypeVar

from dlparse.enums import ConditionComposite, SkillNumber
from dlparse.mono.asset import SkillDataEntry, SkillIdEntry
from .chara import CharaEntryBase
from .entry import CsvExportableEntryBase, HashableEntryBase, JsonExportableEntryBase
from .text import TextEntry

__all__ = ("SkillExportEntryBase",)

T = TypeVar("T")


@dataclass
class SkillExportEntryBase(
    Generic[T], CharaEntryBase, HashableEntryBase, CsvExportableEntryBase, JsonExportableEntryBase, ABC
):
    """Base class for an exported skill data entry."""

    skill_data: InitVar[SkillDataEntry]

    skill_id_entry: InitVar[SkillIdEntry]

    condition_comp: ConditionComposite

    skill_data_to_parse: InitVar[T]

    skill_internal_id: int = field(init=False)
    skill_identifiers: str = field(init=False)
    skill_num: SkillNumber = field(init=False)
    skill_name: TextEntry = field(init=False)
    skill_max_level: int = field(init=False)

    sp_at_max: float = field(init=False)
    sharable: bool = field(init=False)
    ss_cost: int = field(init=False)
    ss_sp: float = field(init=False)

    def __post_init__(
            self, skill_data: SkillDataEntry, skill_id_entry: SkillIdEntry,
            skill_data_to_parse: T
    ):  # pylint: disable=unused-argument
        # ``skill_data_to_parse`` is marked as unused by pylint.
        # However, it will be used by the classes that inherit this class.
        super().__post_init__()

        self.skill_internal_id = skill_id_entry.skill_id
        self.skill_identifiers = skill_id_entry.skill_identifier_labels
        self.skill_num = skill_id_entry.skill_num
        self.skill_name = TextEntry(self.asset_manager.asset_text_multi, skill_data.name_label)
        self.skill_max_level = self.chara_data.max_skill_level(skill_id_entry.skill_num)

        self.sp_at_max = skill_data.get_sp_at_level(self.skill_max_level)
        self.sharable = self.chara_data.ss_skill_id == skill_data.id
        self.ss_cost = self.chara_data.ss_skill_cost
        self.ss_sp = skill_data.get_ss_sp_at_level(self.skill_max_level) if self.sharable else 0

    @property
    def unique_id(self) -> str:
        return (
            f"{self.character_internal_id}{self.skill_internal_id}{self.skill_identifiers}"
            f"{hash(self.condition_comp)}"
        )

    def to_csv_entry(self) -> list[str]:
        """Convert the current data to a csv entry."""
        return [
            self.unique_hash,
            self.character_custom_id,
            self.character_name,
            self.character_internal_id,
            self.character_element,
            self.skill_internal_id,
            self.skill_identifiers,
            self.condition_comp,
            self.sp_at_max,
            self.ss_sp
        ]

    @classmethod
    def csv_header(cls) -> list[str]:
        """Get the header for CSV file."""
        return [
            "Entry Hash",
            "Character ID",
            "Character Name",
            "Character Internal ID",
            "Character Element",
            "Skill Internal ID",
            "Skill Identifier",
            "Conditions",
            "SP (at max lv)",
            "SS SP (at max lv)"
        ]

    def to_json_entry(self) -> dict[str, Any]:
        # Used by the website, DO NOT CHANGE
        return {
            "uniqueHash": self.unique_hash,
            "condition": [condition.value for condition in self.condition_comp.conditions_sorted],
            "chara": super().to_json_entry(),
            "skill": {
                "identifiers": self.skill_identifiers,
                "internalId": self.skill_internal_id,
                "name": self.skill_name.to_json_entry(),
                "spMax": self.sp_at_max,
                "sharable": self.sharable,
                "ssCost": self.ss_cost,
                "ssSp": self.ss_sp
            }
        }
