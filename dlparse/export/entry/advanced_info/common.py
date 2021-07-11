"""Classes for entries that are used in both character and dragon advanced info."""
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from ..skill_atk import AttackingSkillEntry

__all__ = ("OfficialSkillEntry", "UnitSkillEntry", "AbilityInfoEntry", "AdvancedInfoEntryBase")


@dataclass
class OfficialSkillEntry:
    """An entry for a unit skill with official descriptions."""

    icon_path: str
    name: str
    description: str


@dataclass
class UnitSkillEntry:
    """An entry that collects all skills of a unit."""

    official: list[OfficialSkillEntry]
    atk_skills: list[AttackingSkillEntry]


@dataclass
class AbilityInfoEntry:
    """An entry that collects all ability info of a unit."""

    passive: list[str]

    co_ability_global: Optional[str]
    co_ability_chained: Optional[str]


T = TypeVar("T")


@dataclass
class AdvancedInfoEntryBase(Generic[T]):
    """An entry for the advanced info of a dragon."""

    basic: T
    skill: UnitSkillEntry
    ability: AbilityInfoEntry
