"""Models for ability data."""
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, TypeVar

from .effect_base import EffectUnitBase

if TYPE_CHECKING:
    from dlparse.mono.asset import AbilityEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("AbilityData",)

T = TypeVar("T", bound=EffectUnitBase)


@dataclass
class AbilityData:
    """A transformed ability data."""

    asset_manager: InitVar["AssetManager"]

    ability_data: dict[int, "AbilityEntry"]

    _effect_units: set[T] = field(init=False)

    def _init_units(self, asset_manager: "AssetManager"):
        self._effect_units = set()
        for ability_entry in self.ability_data.values():
            self._effect_units.update(ability_entry.to_effect_units(asset_manager))

    def __post_init__(self, asset_manager: "AssetManager"):
        self._init_units(asset_manager)

    @property
    def unknown_condition_ids(self) -> dict[int, int]:
        """
        Get a dict which key is the ability ID and value is the ID of the unknown condition.

        If the ability does not have any unknown condition, an empty dict will be returned.
        """
        return {
            ability_id: ability_entry.condition.condition_code
            for ability_id, ability_entry in self.ability_data.items()
            if ability_entry.condition.is_unknown_condition
        }

    @property
    def unknown_variant_ids(self) -> dict[int, list[int]]:
        """
        Get a dict which key is the ability ID and value is type ID of the unknown variants.

        If the ability does not have any unknown variants, an empty dict will be returned.
        """
        return {
            ability_id: ability_entry.unknown_variant_type_ids
            for ability_id, ability_entry in self.ability_data.items()
            if ability_entry.unknown_variant_type_ids
        }

    @property
    def has_unknown_elements(self) -> bool:
        """Check if the ability data contains any unknown variants or condition."""
        return bool(self.unknown_condition_ids or self.unknown_variant_ids)

    @property
    def effect_units(self) -> set[T]:
        """Get all effect units of the ability."""
        return self._effect_units
