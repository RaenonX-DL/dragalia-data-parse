"""Base entry class for mono behavior."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

__all__ = ("EntryBase", "TextEntryBase")


@dataclass
class EntryBase(ABC):
    """Base class for the entries in the mono behavior assets."""

    @staticmethod
    @abstractmethod
    def parse_raw(data: dict[str, Union[str, int, float]]) -> "EntryBase":
        """Parse a raw data entry to be the asset entry class."""
        raise NotImplementedError()

    @staticmethod
    def parse_datetime(datetime_str: str) -> Optional[datetime]:
        """Parse ``datetime_str`` to be :class:`datetime` if it's not an empty string."""
        return datetime.strptime(datetime_str, "%Y/%m/%d %H:%M:%S") if datetime_str else None


@dataclass
class TextEntryBase(EntryBase, ABC):
    """Base class for an entry containing a representing text."""

    text: str
