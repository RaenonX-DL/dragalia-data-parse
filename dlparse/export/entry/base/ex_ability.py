"""Classes for the EX (Co-ab) and chained EX (CCA) data entries."""
from dataclasses import dataclass, field
from typing import Any

from dlparse.model import ChainedExAbilityData, ExAbilityData
from dlparse.mono.asset import CharaDataEntry
from dlparse.mono.manager import AssetManager
from .effect_ability import AbilityVariantEffectEntry
from .entry import JsonExportableEntryBase
from .type import JsonSchema

__all__ = ("ExAbiltiesEntry",)


@dataclass
class ExAbiltiesEntry(JsonExportableEntryBase):
    """Base class for an entry containing EX (Co-ab) and chained EX (CCA)."""

    asset_manager: AssetManager

    unit_data: CharaDataEntry

    ex_ability_data: ExAbilityData = field(init=False)
    cex_ability_data: ChainedExAbilityData = field(init=False)

    def __post_init__(self):
        self.ex_ability_data = self.asset_manager.transformer_ability.transform_ex_ability(
            self.unit_data.ex_id_at_max_level)
        self.cex_ability_data = self.asset_manager.transformer_ability.transform_chained_ex_ability(
            self.unit_data.cex_id_at_max_level
        )

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "ex": [AbilityVariantEffectEntry.json_schema],
            "chainedEx": [AbilityVariantEffectEntry.json_schema]
        }

    def to_json_entry(self) -> dict[str, Any]:
        # Sort the effect units by its condition and parameter to guarantee deterministic results
        ex_entries = [
            AbilityVariantEffectEntry(self.asset_manager, effect_unit).to_json_entry()
            for effect_unit
            in sorted(
                self.ex_ability_data.effect_units,
                key=lambda unit: (unit.condition_comp, unit.parameter.value)
            )
        ]
        chained_ex_entries = [
            AbilityVariantEffectEntry(self.asset_manager, effect_unit).to_json_entry()
            for effect_unit
            in sorted(
                self.cex_ability_data.effect_units,
                key=lambda unit: (unit.condition_comp, unit.parameter.value)
            )
        ]

        return {
            "ex": ex_entries,
            "chainedEx": chained_ex_entries,
        }
