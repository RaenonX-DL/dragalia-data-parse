"""Error classes used by util functions."""
from typing import TYPE_CHECKING

from .base import AppValueError

if TYPE_CHECKING:
    from dlparse.enums import Language

__all__ = ("PathUnlocalizableError",)


class PathUnlocalizableError(AppValueError):
    """Error to be raised if the path cannot be localized."""

    def __init__(self, path: str, lang: "Language"):
        super().__init__(f"Cannot localize the path `{path}` to language {lang}")
