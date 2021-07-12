"""Extensions for the ability entry."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from dlparse.mono.asset.base import AbilityConditionEntryBase, AbilityVariantEntryBase, MasterEntryBase
from .named import DescribedNameEntry

__all__ = ("AbilityEntryExtension",)

CT = TypeVar("CT", bound=AbilityConditionEntryBase)
VT = TypeVar("VT", bound=AbilityVariantEntryBase)


@dataclass
class AbilityEntryExtension(Generic[CT, VT], DescribedNameEntry, MasterEntryBase, ABC):
    """Base class of an ability entry."""

    condition: CT

    ability_icon_name: str

    @property
    @abstractmethod
    def variants(self) -> list[VT]:
        """
        Get all in-use ability variants as a list.

        Note that this does **not** give the other variants that come from different ability linked by the variants.
        To get all possible variants, call ``get_variants()`` instead.
        """
        raise NotImplementedError()

    @property
    def unknown_variant_type_ids(self) -> list[int]:
        """Get a list of unknown variant type IDs."""
        return [variant.type_id for variant in self.variants if variant.is_unknown_type]
