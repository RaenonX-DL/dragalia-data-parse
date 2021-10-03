"""Enums of the language codes available on the website."""
from enum import Enum

from dlparse.errors import EnumConversionError

__all__ = ("Language",)


class Language(str, Enum):
    """Language enums."""

    CHT = "cht"
    CHS = "chs"
    EN = "en"
    JP = "jp"

    @property
    def locale(self) -> str:
        """
        Convert the language to its corresponding locale.

        Throws ``EnumConversionError`` if the current language is ``Language.JP``
        as it does not have affiliated locale code.

        :raises EnumConversionError: if the language is ``Language.JP``
        """
        if self == Language.CHT:
            return "tw"

        if self == Language.CHS:
            return "cn"

        if self == Language.EN:
            return "en"

        raise EnumConversionError(self, Language, "(Locale code)")

    @property
    def is_main(self) -> bool:
        """Check if this language is the main language (JP)."""
        return self == Language.JP

    @property
    def is_fully_supported(self) -> bool:
        """
        If the language is fully supported.

        Fully supported is defined to have a corresponding UI on the website.
        Also, fully supported languages must be included in every text entry.
        """
        return self in (Language.JP, Language.CHT, Language.EN)

    @classmethod
    def get_all_available_codes(cls) -> list[str]:
        """Get all available language codes."""
        # noinspection PyUnresolvedReferences
        return [enum.value for enum in cls]
