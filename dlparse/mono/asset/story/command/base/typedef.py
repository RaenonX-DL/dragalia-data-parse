"""Type definitions related to story commands."""
from typing import TypedDict

__all__ = ("RawCommand",)


class RawCommand(TypedDict):
    """Schema of a story command in the exported story data."""

    row: int
    command: str
    args: list[str]
