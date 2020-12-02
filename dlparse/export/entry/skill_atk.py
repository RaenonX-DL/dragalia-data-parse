"""Attacking skill data entry classes for export."""
from dataclasses import dataclass, field

from dlparse.model import AttackingSkillDataEntry
from dlparse.mono.asset import TextAsset, CharaDataEntry, SkillIdEntry, SkillDataEntry
from .base import SkillExportEntryBase

__all__ = ("CharaAttackingSkillEntry",)


@dataclass
class CharaAttackingSkillEntry(SkillExportEntryBase[AttackingSkillDataEntry]):
    """A single entry of an attacking skill."""

    skill_total_mods_max: float = field(init=False)
    skill_total_hits_max: int = field(init=False)

    def __post_init__(self, text_asset: TextAsset, chara_data: CharaDataEntry, skill_data: SkillDataEntry,
                      skill_id_entry: SkillIdEntry, skill_data_to_parse: AttackingSkillDataEntry):
        super().__post_init__(text_asset, chara_data, skill_data, skill_id_entry, skill_data_to_parse)

        self.skill_total_mods_max = skill_data_to_parse.total_mod_at_max
        self.skill_total_hits_max = skill_data_to_parse.hit_count_at_max

    def to_csv_entry(self) -> list[str]:
        """Convert the current data to a csv entry."""
        return super().to_csv_entry() + [
            self.skill_total_mods_max,
            str(self.skill_total_hits_max),
        ]

    @classmethod
    def csv_header(cls) -> list[str]:
        """Get the header for CSV file."""
        return super(cls).to_csv_entry() + [
            "Skill Total Mods",
            "Skill Total Hits",
        ]
