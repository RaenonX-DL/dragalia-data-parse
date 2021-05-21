"""Base classes for the data entries to be exported."""
import hashlib
from abc import ABC, abstractmethod
from typing import Any, final

from .type import JsonSchema

__all__ = ("CsvExportableEntryBase", "JsonExportableEntryBase", "HashableEntryBase")


class CsvExportableEntryBase(ABC):
    """Base class for an csv-exportable data entry."""

    @abstractmethod
    def to_csv_entry(self) -> list[str]:
        """Convert the current data to a csv entry."""
        raise NotImplementedError(f"Entry `{self.__class__.__name__}` cannot be converted to a csv entry")

    @classmethod
    @abstractmethod
    def csv_header(cls) -> list[str]:
        """Get the header for CSV file containing this entry."""
        raise NotImplementedError(f"Entry `{cls.__name__}` does not implement a csv header")


class JsonExportableEntryBase(ABC):
    """Base class for an json-exportable data entry."""

    @classmethod
    @property
    @abstractmethod
    def json_schema(cls) -> JsonSchema:
        """Entry JSON schema."""
        raise NotImplementedError(f"Entry `{cls.__name__}` did not define a JSON schema")

    @abstractmethod
    def to_json_entry(self) -> dict[str, Any]:
        """Convert the current data to a json entry."""
        raise NotImplementedError(f"Entry `{self.__class__.__name__}` cannot be converted to a json entry")


class HashableEntryBase(ABC):
    """Base class for an hashable exported data entry."""

    @property
    @abstractmethod
    def unique_id(self) -> str:
        """An ID that uniquely identifies the entry."""
        raise NotImplementedError()

    @property
    @final
    def unique_hash(self):
        """A hash that uniquely identifies this entry."""
        return hashlib.sha256(self.unique_id.encode("utf-8")).hexdigest()
