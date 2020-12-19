"""Class for a single buffing hit."""
from dataclasses import dataclass

from dlparse.mono.asset import ActionComponentBase
from .hit_conv import HitDataEffectConvertible

__all__ = ("BuffingHitData",)


@dataclass
class BuffingHitData(HitDataEffectConvertible[ActionComponentBase]):  # pylint: disable=too-many-ancestors
    """Class for the data of a single buffing hit."""
