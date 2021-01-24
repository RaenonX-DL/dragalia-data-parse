"""Mixin that enables an enum class to be translated."""
from abc import abstractmethod
from enum import Enum

__all__ = ("TranslatableEnumMixin",)


class TranslatableEnumMixin(Enum):
    """Mixin class that allows the members of a enum class to be translated."""

    @property
    @abstractmethod
    def translation_id(self) -> str:
        """Get the translation ID of the enum."""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_all_translatable_members() -> list:
        """Get all translatable enum members."""
        raise NotImplementedError()
