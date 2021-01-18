"""Miscellaneous error classes."""
from enum import Enum
from typing import Any, Type, Union

from .base import AppValueError

__all__ = ("EnumConversionError", "EnumNotFoundError", "OperationInvalidError")


class EnumConversionError(AppValueError):
    """Error to be raised if the enum cannot be converted to either another enum or a string."""

    def __init__(self, enum_to_convert: Enum, enum_cls_src: Type[Enum], enum_cls_dest: Union[Type[Enum], str]):
        super().__init__(f"Cannot convert `{enum_to_convert}` from `{enum_cls_src}` to `{enum_cls_dest}`")


class EnumNotFoundError(AppValueError):
    """Error to be raised if the enum cannot be converted from some other thing to an enum."""

    def __init__(self, enum_cls: Type[Enum], src: Any):
        super().__init__(f"Cannot convert `{src}` to `{enum_cls}`")


class OperationInvalidError(AppValueError):
    """Error to be raised if the operation is invalid."""
