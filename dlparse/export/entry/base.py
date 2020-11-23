"""Base classes for the data entries to be exported."""
from abc import ABC, abstractmethod

__all__ = ("ExportEntryBase",)


class ExportEntryBase(ABC):
    """Base class for an exported data entry."""

    @property
    @abstractmethod
    def unique_id(self):
        """An ID that uniquely identifies the entry."""
        raise NotImplementedError()

    def to_csv_entry(self) -> list[str]:
        """Convert the current data to a csv entry."""
        raise NotImplementedError(f"Entry `{self.__class__.__name__}` cannot be converted to a csv entry")

    @classmethod
    def csv_header(cls) -> list[str]:
        """Get the header for CSV file containing this entry."""
        raise NotImplementedError(f"Entry `{cls.__name__}` does not implement a csv header")
