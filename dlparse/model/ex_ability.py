"""Models for ex ability data."""
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .ability_common import AbilityDataBase
from .ability_var_common import AbilityVariantEffectUnit, ability_to_effect_units
from .ex_ability_var import make_payload_ex_ability

if TYPE_CHECKING:
    from dlparse.mono.asset import ExAbilityEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("ExAbilityData",)


@dataclass
class ExAbilityData(AbilityDataBase):
    """A transformed ex ability data."""

    ex_ability_data: "ExAbilityEntry"

    _effect_units: set[AbilityVariantEffectUnit] = field(init=False)

    def _init_units(self, asset_manager: "AssetManager"):
        payload = make_payload_ex_ability(self.ex_ability_data)

        self._effect_units = ability_to_effect_units(self.ex_ability_data, asset_manager, payload)

    @property
    def unknown_condition_ids(self) -> dict[int, int]:
        if self.ex_ability_data.condition.is_unknown_condition:
            return {self.ex_ability_data.id: self.ex_ability_data.condition.condition_code}

        return {}

    @property
    def unknown_variant_ids(self) -> dict[int, list[int]]:
        if unknown_variants := self.ex_ability_data.unknown_variant_type_ids:
            return {self.ex_ability_data.id: unknown_variants}

        return {}
