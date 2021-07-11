"""Classes for the EX (Co-ab) and chained EX (CCA) data entries."""
from dataclasses import dataclass
from typing import Any

from dlparse.model import ChainedExAbilityData, ExAbilityData
from .base import AbilityVariantEffectEntry, JsonExportableEntryBase, JsonSchema, UnitEntryBase

__all__ = ("CharaExAbiltiesEntry",)


@dataclass
class CharaExAbiltiesEntry(UnitEntryBase, JsonExportableEntryBase):
    """A single entry containing EX (Co-ab) and chained EX (CCA) of a character."""

    ex_ability_data: ExAbilityData
    cex_ability_data: ChainedExAbilityData

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return super().json_schema | {
            "chara": UnitEntryBase.json_schema,
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
            "chara": super().to_json_entry(),
            "ex": ex_entries,
            "chainedEx": chained_ex_entries,
        }
