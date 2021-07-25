"""Enums for all attacking action types."""
from enum import Enum, auto

__all__ = ("AttackActionType",)


class AttackActionType(Enum):
    """Enums for the attacking action of an unit."""

    NORMAL_ATTACK = auto()
    FS = auto()
