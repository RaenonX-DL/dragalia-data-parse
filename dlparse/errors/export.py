"""Exporting errors."""

from .base import AppValueError

__all__ = ("MissingTextError",)


class MissingTextError(AppValueError):
    """Error to be raised if no texts have been recorded during text entry construction."""

    def __init__(self, labels: list[str], lang_code: str):
        super().__init__(f"None of the labels in {labels} is available in language code `{lang_code}`")
