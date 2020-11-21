"""Skill data entry classes for export."""
from dataclasses import dataclass

from dlparse.enums import SkillCondition, Element

__all__ = ("CharaAttackingSkillEntry",)


@dataclass
class CharaAttackingSkillEntry:
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
    ``skill_identifier``

        Identifier (not the name) of the skill.

    ``skill_name``

        Actual in-game name of the skill.

    ``skill_conditions``

        Conditions of the skill.

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

    skill_identifier: str
    skill_name: str
    skill_conditions: tuple[SkillCondition]
    skill_total_mods_max: float
    skill_total_hits_max: int
    skill_max_lv: int

    def to_csv_entry(self) -> list[str]:
        """Convert the current data to a csv entry."""
        return [
            self.character_custom_id,
            self.character_name,
            self.character_internal_id,
            self.character_element,
            self.skill_identifier,
            self.skill_name,
            self.skill_conditions,
            self.skill_total_mods_max,
            self.skill_total_hits_max,
            self.skill_max_lv
        ]

    @staticmethod
    def csv_header() -> list[str]:
        """Get the header for CSV file."""
        return [
            "Character ID",
            "Character Name",
            "Character Internal ID",
            "Character Element",
            "Skill Identifier",
            "Skill Name",
            "Skill Conditions",
            "Skill Total Mods",
            "Skill Total Hits",
            "Skill Max Lv.",
        ]
