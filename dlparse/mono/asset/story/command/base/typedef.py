"""Type definitions related to story commands."""
from typing import TypedDict

__all__ = ("RawCommand",)


class RawCommand(TypedDict):
    row: int
    command: str
    args: list[str]
