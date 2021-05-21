"""Exporting entry for a skill identifier info."""
from dataclasses import dataclass

from .base import NamedEntry

__all__ = ("SkillIdentifierEntry",)


@dataclass
class SkillIdentifierEntry(NamedEntry):
    """A single entry of a skill identifier info."""
