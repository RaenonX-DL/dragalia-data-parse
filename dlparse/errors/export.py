"""Exporting errors."""
from typing import Optional

from .base import AppValueError

__all__ = ("MissingTextError",)


class MissingTextError(AppValueError):
    """Error to be raised if no texts have been recorded during text entry construction."""

    def __init__(self, labels: list[str], lang_code: str, message: Optional[str] = None):
        super().__init__(f"None of the labels in {labels} is available in language code `{lang_code}`: {message}")

        self._lang_code = lang_code
        self._labels = labels

    @property
    def lang_code(self) -> str:
        """Language code that causes this error."""
        return self._lang_code

    @property
    def labels(self) -> list[str]:
        """Missing text labels."""
        return self._labels
