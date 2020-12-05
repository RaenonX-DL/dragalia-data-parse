"""Base class for a single hit."""
from abc import ABC
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from dlparse.enums import SkillCondition
from dlparse.mono.asset import ActionComponentBase, HitAttrEntry

__all__ = ("HitData",)

T = TypeVar("T", bound=ActionComponentBase)


@dataclass
class HitData(Generic[T], ABC):
    """Class for the data of a single hit."""

    hit_attr: HitAttrEntry
    action_id: int
    action_component: Optional[T]
    pre_condition: SkillCondition
    """
    Condition for the hits to be effective.

    This may come from:
    - Condition from the action component
    - Ability condition embedded on the skill data
    """
