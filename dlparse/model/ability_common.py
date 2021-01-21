"""
Common implementations for the ability data class across different types.

Types of the ability include but not limited to:

- Ability
- EX Ability
"""
from abc import ABC, abstractmethod
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from .ability_var_common import AbilityVariantEffectUnit

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("AbilityDataBase",)


@dataclass
class AbilityDataBase(ABC):
    """Base class of a transformed ability data."""

    asset_manager: InitVar["AssetManager"]

    _effect_units: set[AbilityVariantEffectUnit] = field(init=False)

    @abstractmethod
    def _init_units(self, asset_manager: "AssetManager"):
        """
        Initializes the variable ``_effect_units``.

        This will be called during class initialization (``__post_init__()``).
        """
        raise NotImplementedError()

    def __post_init__(self, asset_manager: "AssetManager"):
        self._init_units(asset_manager)

    @property
    @abstractmethod
    def unknown_condition_ids(self) -> dict[int, int]:
        """
        Get a dict which key is the ability ID and value is the ID of the unknown condition.

        If the ability does not have any unknown condition, an empty dict will be returned.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def unknown_variant_ids(self) -> dict[int, list[int]]:
        """
        Get a dict which key is the ability ID and value is type ID of the unknown variants.

        If the ability does not have any unknown variants, an empty dict will be returned.
        """
        raise NotImplementedError()

    @property
    def has_unknown_elements(self) -> bool:
        """Check if the ability data contains any unknown variants or condition."""
        return bool(self.unknown_condition_ids or self.unknown_variant_ids)

    @property
    def effect_units(self) -> set[AbilityVariantEffectUnit]:
        """Get all effect units of the ability."""
        return self._effect_units
