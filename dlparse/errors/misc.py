"""Miscellaneous error classes."""
from enum import Enum
from typing import Any, TYPE_CHECKING, Type, Union

from .base import AppValueError

if TYPE_CHECKING:
    from dlparse.enums import ConditionComposite

__all__ = (
    "EnumConversionError", "EnumNotFoundError", "ImageNotFoundError", "OperationInvalidError",
    "ConditionsUnavailableError",
)


class EnumConversionError(AppValueError):
    """Error to be raised if the enum cannot be converted to either another enum or a string."""

    def __init__(self, enum_to_convert: Enum, enum_cls_src: Type[Enum], enum_cls_dest: Union[Type[Enum], str]):
        super().__init__(f"Cannot convert `{enum_to_convert}` from `{enum_cls_src}` to `{enum_cls_dest}`")


class EnumNotFoundError(AppValueError):
    """Error to be raised if the enum cannot be converted from some other thing to an enum."""

    def __init__(self, enum_cls: Type[Enum], src: Any):
        super().__init__(f"Cannot convert `{src}` to `{enum_cls}`")


class ImageNotFoundError(AppValueError):
    """Error to be raised if the image for an enum is not found."""

    def __init__(self, enum: Enum):
        super().__init__(f"Image for `{enum}` not found")


class OperationInvalidError(AppValueError):
    """Error to be raised if the operation is invalid."""


class ConditionsUnavailableError(AppValueError):
    """Error to be raised if the given conditions is unavailable for further operations."""

    def __init__(self, conditions: "ConditionComposite"):
        super().__init__(f"Conditions `{conditions.conditions_sorted}` is unavailable")
