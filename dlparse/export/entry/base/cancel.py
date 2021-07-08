"""Unit of a skill cancellation info."""
from dataclasses import dataclass
from typing import Any

from dlparse.enums import ConditionComposite, SkillCancelAction
from .entry import JsonExportableEntryBase
from .type import JsonSchema

__all__ = ("SkillCancelInfoEntry",)


@dataclass
class SkillCancelInfoEntry(JsonExportableEntryBase):
    """A single entry representing a single skill cancellation info."""

    action: SkillCancelAction
    time: float

    pre_conditions: ConditionComposite

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "action": int,
            "time": float,
            "conditions": [int],
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "action": self.action.value,
            "time": self.time,
            "conditions": [condition.value for condition in self.pre_conditions.conditions_sorted],
        }
