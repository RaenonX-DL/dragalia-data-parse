"""Class for a single buffing hit."""
from dataclasses import dataclass

from dlparse.mono.asset import ActionComponentBase
from .hit_unit import UnitsConvertibleHitData

__all__ = ("BuffingHitData",)


@dataclass
class BuffingHitData(UnitsConvertibleHitData[ActionComponentBase]):  # pylint: disable=too-many-ancestors
    """Class for the data of a single buffing hit."""
