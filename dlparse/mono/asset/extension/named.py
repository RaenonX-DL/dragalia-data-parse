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

    @property
    def name_labels(self) -> list[str]:
        """
        Get a list of name labels for getting the actual name.

        Note that the first one should be used first to get the character name. The order matters.
        """
        return [self.name_label_2, self.name_label]
