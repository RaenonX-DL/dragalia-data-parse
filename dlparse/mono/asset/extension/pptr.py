"""Interface for an ``PPtr`` (file pointer)."""
from dataclasses import dataclass

__all__ = ("PPtr",)


@dataclass
class PPtr:
    """Class for an ``PPtr``."""

    file_id: int
    path_id: int

    @staticmethod
    def from_dict(pptr: dict[str, int]) -> "PPtr":
        """Initialize a :class:`PPtr` from :class:`dict`."""
        return PPtr(pptr["m_FileID"], pptr["m_PathID"])
