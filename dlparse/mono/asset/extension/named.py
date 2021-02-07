"""Interface for the named entry."""
from abc import ABC
from dataclasses import dataclass

__all__ = ("NamedEntry",)


@dataclass
class NamedEntry(ABC):
    """Interface for a named data entry."""

    name_label: str
    name_label_2: str
    emblem_id: int
