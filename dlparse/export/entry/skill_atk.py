"""Attacking skill data entry classes for exporting."""
from dataclasses import dataclass, field
from typing import Any

from dlparse.enums import BuffParameter, ConditionCategories
from dlparse.model import AttackingSkillDataEntry
from dlparse.mono.asset import SkillDataEntry, SkillIdEntry
from dlparse.utils import remove_duplicates_preserve_order
from .base import JsonExportableEntryBase, JsonSchema, SkillExportEntryBase

__all__ = ("CharaAttackingSkillEntry",)


@dataclass
class SkillBuffCountBoostEntry(JsonExportableEntryBase):
    """A single entry representing the mods increment according to the user's buff count."""

    rate_each: float

    rate_in_effect: float
    rate_limit: float

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "each": float,
            "inEffect": float,
            "limit": float
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "each": self.rate_each,
            "inEffect": self.rate_in_effect,
            "limit": self.rate_limit
        }


@dataclass
class SkillBuffFieldBoostEntry(JsonExportableEntryBase):
    """A single entry representing the mods increment according to the user's buff field."""

    rate_by_self: float
    rate_by_ally: float

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "self": float,
            "ally": float
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "self": self.rate_by_self,
            "ally": self.rate_by_ally
        }


@dataclass(unsafe_hash=True)
class SkillAfflictionEntry(JsonExportableEntryBase):
    """A single entry for a single affliction of the skill."""

    status_condition_code: int
    status_icon: str
    action_time: float
    probability_pct: float
    duration: float
    stackable: bool

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "statusConditionCode": int,
            "statusIcon": str,
            "actionTime": float,
            "probabilityPct": float,
            "duration": float,
            "stackable": bool,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "statusConditionCode": self.status_condition_code,
            "statusIcon": self.status_icon,
            "actionTime": self.action_time,
            "probabilityPct": self.probability_pct,
            "duration": self.duration,
            "stackable": self.stackable,
        }


@dataclass
class CharaAttackingSkillEntry(SkillExportEntryBase[AttackingSkillDataEntry]):
    """A single entry of an attacking skill."""

    skill_mods_max: list[float] = field(init=False)
    skill_crisis_max: list[float] = field(init=False)
    skill_total_mods_max: float = field(init=False)
    skill_total_hits_max: int = field(init=False)

    affliction_data_max: list[SkillAfflictionEntry] = field(init=False)
    debuff_data_max: list[tuple[BuffParameter, float, float, float, bool]] = field(init=False)

    dispel_max: bool = field(init=False)
    dispel_timing_max: list[float] = field(init=False)

    buff_count_data_max: list[SkillBuffCountBoostEntry] = field(init=False)
    buff_field_data_max: SkillBuffFieldBoostEntry = field(init=False)

    def __post_init__(
            self, skill_data: SkillDataEntry, skill_id_entry: SkillIdEntry,
            skill_data_to_parse: AttackingSkillDataEntry
    ):
        super().__post_init__(skill_data, skill_id_entry, skill_data_to_parse)

        # [SPECIAL] Leave for testing purpose, but not exported as json
        self.skill_total_mods_max = skill_data_to_parse.total_mod_at_max

        # Get basic info
        self.skill_total_hits_max = skill_data_to_parse.hit_count_at_max
        self.skill_mods_max = skill_data_to_parse.mods_at_max
        self.skill_crisis_max = skill_data_to_parse.crisis_mods[-1]

        # Get affliction and debuff data
        afflictions = []
        for affliction in skill_data_to_parse.afflictions[-1]:
            afflictions.append(SkillAfflictionEntry(
                status_condition_code=ConditionCategories.target_status.convert_reversed(affliction.status).value,
                status_icon=affliction.status.icon_name,
                action_time=affliction.time,
                probability_pct=affliction.probability_pct,
                duration=affliction.duration_sec,
                stackable=affliction.stackable
            ))
        self.affliction_data_max = remove_duplicates_preserve_order(afflictions)
        self.debuff_data_max = remove_duplicates_preserve_order([
            (debuff.parameter, debuff.probability_pct, debuff.rate, debuff.duration_sec, debuff.stackable)
            for debuff in skill_data_to_parse.debuffs[-1]
        ])

        # Get dispel data
        self.dispel_max = skill_data_to_parse.dispel_buff_at_max
        self.dispel_timing_max = skill_data_to_parse.dispel_timings[-1]

        # Get buff data
        self.buff_count_data_max = [
            SkillBuffCountBoostEntry(
                rate_each=buff_count_data.rate_base,
                rate_in_effect=buff_count_data.in_effect_rate,
                rate_limit=buff_count_data.rate_limit
            )
            for buff_count_data in skill_data_to_parse.buff_count_boost_mtx[-1]
        ]
        buff_field_data = skill_data_to_parse.buff_field_boost_mtx[-1]
        self.buff_field_data_max = SkillBuffFieldBoostEntry(buff_field_data.rate_by_self, buff_field_data.rate_by_ally)

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        schema = super().json_schema

        schema["skill"].update({
            "modsMax": [float],
            "crisisMax": [float],
            "hitsMax": int,
            "afflictions": [SkillAfflictionEntry.json_schema],
            "buffCountBoost": [SkillBuffCountBoostEntry.json_schema],
            "buffZoneBoost": SkillBuffFieldBoostEntry.json_schema,
            "dispelMax": bool,
            "dispelTimingMax": [float]
        })

        return schema

    def to_json_entry(self) -> dict[str, Any]:
        json_dict = super().to_json_entry()

        json_dict["skill"].update({
            "modsMax": self.skill_mods_max,
            "crisisMax": self.skill_crisis_max,
            "hitsMax": self.skill_total_hits_max,
            "afflictions": [affliction_data.to_json_entry() for affliction_data in self.affliction_data_max],
            "buffCountBoost": [buff_count_data.to_json_entry() for buff_count_data in self.buff_count_data_max],
            "buffZoneBoost": self.buff_field_data_max.to_json_entry(),
            "dispelMax": self.dispel_max,
            "dispelTimingMax": self.dispel_timing_max
        })

        return json_dict
