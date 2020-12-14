"""Models for ability data."""
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dlparse.mono.asset import AbilityEntry

__all__ = ("AbilityData",)


@dataclass
class AbilityData:
    """A transformed ability data."""

    ability_data: list["AbilityEntry"]
