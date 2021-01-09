"""Miscellaneous error classes."""
from enum import Enum
from typing import Type, Union

from .base import AppValueError

__all__ = ("EnumConversionError", "OperationInvalidError")


class EnumConversionError(AppValueError):
    """Error to be raised if the enum cannot be converted."""

    def __init__(self, enum_to_convert: Enum, enum_cls_src: Type[Enum], enum_cls_dest: Union[Type[Enum], str]):
        super().__init__(f"Cannot convert `{enum_to_convert}` "
                         f"from `{enum_cls_src}` to `{enum_cls_dest}`")


class OperationInvalidError(AppValueError):
    """Error to be raised if the operation is invalid."""
