"""Attacking skill data entry classes for exporting."""
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from dlparse.enums import BuffParameter, ConditionCategories
from dlparse.model import AttackingSkillDataEntry
from dlparse.mono.asset import CharaDataEntry, SkillDataEntry, SkillIdEntry
from .base import JsonExportableEntryBase
from .base_skill import SkillExportEntryBase

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("CharaAttackingSkillEntry",)


@dataclass(unsafe_hash=True)
class SkillAfflictionEntry(JsonExportableEntryBase):
    """A single entry for a single affliction of the skill."""

    status_condition_code: int
    status_image: str
    action_time: float
    probability_pct: float
    duration: float
    stackable: bool

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "statusConditionCode": self.status_condition_code,
            "statusImage": self.status_image,
            "actionTime": self.action_time,
            "probabilityPct": self.probability_pct,
            "duration": self.duration,
            "stackable": self.stackable,
        }


@dataclass
class CharaAttackingSkillEntry(SkillExportEntryBase[AttackingSkillDataEntry]):
    """A single entry of an attacking skill."""

    skill_mods_max: list[float] = field(init=False)
    skill_total_mods_max: float = field(init=False)
    skill_total_hits_max: int = field(init=False)

    affliction_data_max: list[SkillAfflictionEntry] = field(init=False)
    debuff_data_max: list[tuple[BuffParameter, float, float, float, bool]] = field(init=False)

    def __post_init__(
            self, asset_manager: "AssetManager", chara_data: CharaDataEntry, skill_data: SkillDataEntry,
            skill_id_entry: SkillIdEntry, skill_data_to_parse: AttackingSkillDataEntry
    ):
        super().__post_init__(asset_manager, chara_data, skill_data, skill_id_entry, skill_data_to_parse)

        self.skill_mods_max = skill_data_to_parse.mods_at_max
        self.skill_total_mods_max = skill_data_to_parse.total_mod_at_max
        self.skill_total_hits_max = skill_data_to_parse.hit_count_at_max

        afflictions = []
        for affliction in skill_data_to_parse.afflictions[-1]:
            afflictions.append(SkillAfflictionEntry(
                status_condition_code=ConditionCategories.target_status.convert_reversed(affliction.status).value,
                status_image=affliction.status.icon_name,
                action_time=affliction.time,
                probability_pct=affliction.probability_pct,
                duration=affliction.duration_time,
                stackable=affliction.stackable
            ))

        self.affliction_data_max = list(dict.fromkeys(afflictions))
        self.debuff_data_max = list(dict.fromkeys([
            (debuff.parameter, debuff.probability_pct, debuff.rate, debuff.duration_time, debuff.stackable)
            for debuff in skill_data_to_parse.debuffs[-1]
        ]))

    def to_csv_entry(self) -> list[str]:
        """Convert the current data to a csv entry."""
        return super().to_csv_entry() + [
            self.skill_total_mods_max,
            str(self.skill_total_hits_max),
            self.affliction_data_max,
            self.debuff_data_max
        ]

    @classmethod
    def csv_header(cls) -> list[str]:
        """Get the header for CSV file."""
        return super().csv_header() + [
            "Skill Total Mods",
            "Skill Total Hits",
            "Afflictions",
            "Debuffs"
        ]

    def to_json_entry(self) -> dict[str, Any]:
        # Synced with the website, DO NOT CHANGE
        json_dict = super().to_json_entry()

        json_dict["skill"].update({
            "totalModsMax": self.skill_total_mods_max,
            "modsMax": self.skill_mods_max,
            "hitsMax": self.skill_total_hits_max,
            "afflictions": [affliction_data.to_json_entry() for affliction_data in self.affliction_data_max]
        })

        return json_dict
