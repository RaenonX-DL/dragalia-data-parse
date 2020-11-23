"""Base error classes."""
from abc import ABC

__all__ = ("AppValueError", "AssetParsingError", "EntryNotFoundError")


class AppValueError(ValueError, ABC):
    """
    Value error base class for the application.

    All value errors of the application should inherit this class.
    """


class AssetParsingError(AppValueError, ABC):
    """
    Base error class for the errors when parsing the data.

    All errors related to data parsing should inherit this class.
    """


class EntryNotFoundError(AppValueError, ABC):
    """
    Base error class to be raised if the mono data entry is not found.

    All asset entry not found errors should inherit this class.
    """
