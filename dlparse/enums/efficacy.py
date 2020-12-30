"""Enums of efficacy types."""
from enum import Enum

__all__ = ("EfficacyType",)


class EfficacyType(Enum):
    """
    Action condition efficacy type.

    This can be found in the field ``_EfficacyType`` of the action conditions.
    """

    UNKNOWN = -1

    ADD = 0
    REMOVE_ALL_TYPE = 1  # ?
    REMOVE_STACK = 2  # ?
    REMOVE_ALL_BUFF = 97
    REMOVE_ALL_DEBUFF = 98
    REMOVE_ALL_STATUS = 99
    DISPEL = 100

    @classmethod
    def _missing_(cls, value):
        return EfficacyType.UNKNOWN
