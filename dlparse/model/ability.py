"""Models for ability data."""
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .ability_common import AbilityDataBase
from .ability_var import make_payload_ability
from .ability_var_common import ability_to_effect_units

if TYPE_CHECKING:
    from dlparse.mono.asset import AbilityEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("AbilityData",)


@dataclass
class AbilityData(AbilityDataBase):
    """A transformed ability data."""

    ability_data: dict[int, "AbilityEntry"]

    is_chained_ex: bool = False

    def _init_units(self, asset_manager: "AssetManager"):
        self._effect_units = set()
        for ability_entry in self.ability_data.values():
            payload = make_payload_ability(ability_entry, is_chained_ex=self.is_chained_ex)

            self._effect_units.update(ability_to_effect_units(ability_entry, asset_manager, payload))

    @property
    def unknown_condition_ids(self) -> dict[int, int]:
        return {
            ability_id: ability_entry.condition.condition_code
            for ability_id, ability_entry in self.ability_data.items()
            if ability_entry.condition.is_unknown_condition
        }

    @property
    def unknown_variant_ids(self) -> dict[int, list[int]]:
        return {
            ability_id: ability_entry.unknown_variant_type_ids
            for ability_id, ability_entry in self.ability_data.items()
            if ability_entry.unknown_variant_type_ids
        }
