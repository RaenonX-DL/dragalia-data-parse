"""Interface for the named entry."""
from abc import ABC

__all__ = ("NamedEntry",)

from dataclasses import dataclass


@dataclass
class NamedEntry(ABC):
    """Interface for a named data entry."""

    name_label: str
    name_label_2: str
    emblem_id: int
