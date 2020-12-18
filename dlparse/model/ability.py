"""Models for ability data."""
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, TypeVar

from .effect_base import EffectUnitBase

if TYPE_CHECKING:
    from dlparse.mono.asset import AbilityEntry, AbilityLimitGroupAsset

__all__ = ("AbilityData",)

T = TypeVar("T", bound=EffectUnitBase)


@dataclass
class AbilityData:
    """A transformed ability data."""

    asset_ability_limit: InitVar["AbilityLimitGroupAsset"]  # Used for recording the max possible value

    ability_data: dict[int, "AbilityEntry"]

    _effect_units: set[T] = field(init=False)

    def _init_units(self, asset_ability_limit: "AbilityLimitGroupAsset"):
        self._effect_units = set()
        for ability_entry in self.ability_data.values():
            self._effect_units.update(ability_entry.to_effect_units(asset_ability_limit))

    def __post_init__(self, asset_ability_limit: "AbilityLimitGroupAsset"):
        self._init_units(asset_ability_limit)

    @property
    def has_unknown_condition(self):
        """Check if the ability data contains any unknown condition."""
        return any(ability_entry.is_unknown_condition for ability_entry in self.ability_data.values())

    @property
    def has_unknown_variants(self):
        """Check if the ability data contains any unknown variants."""
        return any(ability_entry.has_unknown_elements for ability_entry in self.ability_data.values())

    @property
    def has_unknown_elements(self) -> bool:
        """Check if the ability data contains any unknown variants or condition."""
        return self.has_unknown_condition or self.has_unknown_variants

    @property
    def effect_units(self) -> set[T]:
        """Get all effect units of the ability."""
        return self._effect_units
