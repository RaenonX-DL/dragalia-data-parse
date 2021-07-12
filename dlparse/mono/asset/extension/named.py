"""Interface for the named entries."""
from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

from dlparse.enums import Language
from dlparse.errors import TextLabelNotFoundError

if TYPE_CHECKING:
    from dlparse.mono.asset import TextAssetMultilingual

__all__ = ("UnitNameEntry",)


@dataclass
class UnitNameEntry(ABC):
    """Interface for a named data entry."""

    name_label: str
    name_label_2: str
    emblem_id: int

    @property
    def name_labels(self) -> list[str]:
        """
        Get a list of name labels for getting the actual name.

        Note that the first one should be used first to get the character name. The order matters.
        """
        return [self.name_label_2, self.name_label]

    def get_name(self, text_asset: "TextAssetMultilingual", language: Language = Language.JP) -> str:
        """Get the unit name in ``language``."""
        try:
            return text_asset.get_text(language.value, self.name_label_2)
        except TextLabelNotFoundError:
            return text_asset.get_text(language.value, self.name_label)
