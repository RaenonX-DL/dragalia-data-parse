"""Base class for a single hit."""
from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional

from dlparse.enums import SkillCondition
from dlparse.mono.asset import HitAttrEntry, ActionComponentBase

__all__ = ("HitData",)

T = TypeVar("T", bound=ActionComponentBase)


@dataclass
class HitData(Generic[T], ABC):
    """Class for the data of a single hit."""

    hit_attr: HitAttrEntry
    action_component: Optional[T]
    pre_condition: SkillCondition
