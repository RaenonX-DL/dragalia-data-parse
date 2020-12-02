"""Skill data entry classes for export."""
import hashlib
from dataclasses import dataclass

from dlparse.enums import SkillConditionComposite, Element
from .base import ExportEntryBase

__all__ = ("CharaAttackingSkillEntry",)


@dataclass
class CharaAttackingSkillEntry(ExportEntryBase):
    """
    A single entry of an attacking skill.

    The example data below will be the data from Wedding Elisanne.

    Character
    =========

    ``character_custom_id``

        ID used for identifying the character in the application.
        This ID is based on the base ID and the variation ID of the character. Example value: 100002/6.

    ``character_name``

        Name used to **uniquely** identifies the character in-game.
        For example: 耶魯菲莉絲（花嫁Ver.）.

    ``character_internal_id``

        ID used in ``CharaData.json``. For example: 10150302.

    ``character_element``

        Element of the character.

    Skill Info
    ==========
    ``skill_internal_id``

        ID used in ``SkillData.json``. For example: 101503021 for S1; 101503022 for S2.

    ``skill_identifier``

        Identifier (not the name) of the skill.

    ``skill_unique_id``

        An unique ID identifies the skill and mode combined.

    ``skill_name``

        Actual in-game name of the skill.

    ``skill_condition_comp``

        Condition composite of the skill entry.

    ``skill_total_mods_max``

        Damage modifier of the skill at the maximum level.

    ``skill_total_hits_max``

        Total hits of the skill at the maximum level.

    ``skill_max_lv``

        Maximum level of the skill.
    """

    character_custom_id: str
    character_name: str
    character_internal_id: int
    character_element: Element

    skill_internal_id: int
    skill_identifier: str
    skill_name: str
    skill_condition_comp: SkillConditionComposite
    skill_total_mods_max: float
    skill_total_hits_max: int
    skill_max_lv: int

    @property
    def unique_id(self):
        return hashlib.sha256(
            f"{self.character_internal_id}{self.skill_internal_id}{self.skill_identifier}"
            f"{hash(self.skill_condition_comp)}".encode("utf-8")
        ).hexdigest()

    def to_csv_entry(self) -> list[str]:
        """Convert the current data to a csv entry."""
        return [
            self.unique_id,
            self.character_custom_id,
            self.character_name,
            self.character_internal_id,
            self.character_element,
            self.skill_internal_id,
            self.skill_name,
            self.skill_condition_comp,
            self.skill_total_mods_max,
            self.skill_total_hits_max,
            self.skill_max_lv
        ]

    @classmethod
    def csv_header(cls) -> list[str]:
        """Get the header for CSV file."""
        return [
            "Entry ID",
            "Character ID",
            "Character Name",
            "Character Internal ID",
            "Character Element",
            "Skill Internal ID",
            "Skill Name",
            "Skill Conditions",
            "Skill Total Mods",
            "Skill Total Hits",
            "Skill Max Lv.",
        ]
