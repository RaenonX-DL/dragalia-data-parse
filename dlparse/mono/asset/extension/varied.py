"""
Interface for the varied entry.

Currently known cases:
- Character data
- Dragon data
"""
from abc import ABC
from dataclasses import dataclass

__all__ = ("VariedEntry", "VariationIdentifier")

VariationIdentifier = tuple[int, int]


@dataclass
class VariedEntry(ABC):
    """Interface for a varied entry."""

    base_id: int
    variation_id: int

    @property
    def var_identifier(self) -> VariationIdentifier:
        """Get the variation identifier of this entry."""
        return self.base_id, self.variation_id
