"""Class for a single buffing hit."""
from dataclasses import dataclass

from dlparse.mono.asset import ActionComponentBase
from .hit_base import HitData

__all__ = ("BuffingHitData",)


@dataclass
class BuffingHitData(HitData[ActionComponentBase]):
    """Class for the data of a single buffing hit."""
