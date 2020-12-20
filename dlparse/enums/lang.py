"""Enums for the language codes available on the website."""
from enum import Enum

__all__ = ("Language",)


class Language(str, Enum):
    """Language enums."""

    CHT = "cht"
    EN = "en"
    JP = "jp"

    @classmethod
    def get_all_available_codes(cls) -> list[str]:
        """Get all available language codes."""
        # noinspection PyUnresolvedReferences
        return [enum.value for enum in cls]
