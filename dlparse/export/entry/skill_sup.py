"""Supportive skill data entry classes for exporting."""
from dataclasses import dataclass, field

from dlparse.enums import BuffParameter, HitTargetSimple
from dlparse.model import HitActionConditionEffectUnit
from dlparse.mono.asset import SkillDataEntry, SkillIdEntry
from .base import SkillExportEntryBase

__all__ = ("CharaSupportiveSkillEntry",)


@dataclass
class CharaSupportiveSkillEntry(SkillExportEntryBase[HitActionConditionEffectUnit]):
    """A single entry of a supportive skill."""

    target: HitTargetSimple = field(init=False)
    buff_parameter: BuffParameter = field(init=False)
    rate: float = field(init=False)
    duration_count: float = field(init=False)
    duration_sec: float = field(init=False)
    max_stack_count: int = field(init=False)

    def __post_init__(
            self, skill_data: SkillDataEntry, skill_id_entry: SkillIdEntry,
            skill_data_to_parse: HitActionConditionEffectUnit
    ):
        super().__post_init__(skill_data, skill_id_entry, skill_data_to_parse)

        self.target = skill_data_to_parse.target
        self.buff_parameter = skill_data_to_parse.parameter
        self.rate = skill_data_to_parse.rate
        self.duration_count = skill_data_to_parse.duration_count
        self.duration_sec = skill_data_to_parse.duration_sec
        self.max_stack_count = skill_data_to_parse.max_stack_count

    @property
    def unique_id(self) -> str:
        return f"{super().unique_id}{self.buff_parameter}{self.rate}"
