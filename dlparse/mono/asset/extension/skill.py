"""Interface for the entry that has skills."""
from abc import ABC
from dataclasses import dataclass

__all__ = ("SkillEntry",)


@dataclass
class SkillEntry(ABC):
    """Interface for a data entry with skills."""

    skill_1_id: int
    skill_2_id: int
