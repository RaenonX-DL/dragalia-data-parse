"""
Interface for the varied entry.

Currently known cases:
- Character data
- Dragon data
"""
from abc import ABC
from dataclasses import dataclass

__all__ = ("VariedEntry",)


@dataclass
class VariedEntry(ABC):
    """Interface for a varied entry."""

    base_id: int
    variation_id: int
