"""Unit of a skill cancellation info."""
from dataclasses import InitVar, dataclass, field
from typing import Any

from dlparse.enums import ConditionComposite, SkillCancelAction
from dlparse.model import SkillCancelActionUnit
from .entry import JsonExportableEntryBase
from .type import JsonSchema

__all__ = ("SkillCancelInfoEntry",)


@dataclass
class SkillCancelInfoEntry(JsonExportableEntryBase):
    """A single entry representing a single skill cancellation info."""

    cancel_unit: InitVar[SkillCancelActionUnit]

    action: SkillCancelAction = field(init=False)
    time: float = field(init=False)

    pre_conditions: ConditionComposite = field(init=False)

    def __post_init__(self, cancel_unit: SkillCancelActionUnit):
        self.action = cancel_unit.action
        self.time = cancel_unit.time
        self.pre_conditions = cancel_unit.pre_conditions

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
