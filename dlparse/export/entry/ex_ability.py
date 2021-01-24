"""Classes for the EX (Co-ab) and chained EX (CCA) data entries."""
from dataclasses import dataclass
from typing import Any

from dlparse.model import ChainedExAbilityData, ExAbilityData
from .base import CharaEntryBase, JsonExportableEntryBase
from .effect import AbilityVariantEffectEntry

__all__ = ("CharaExAbiltiesEntry",)


@dataclass
class CharaExAbiltiesEntry(CharaEntryBase, JsonExportableEntryBase):
    """A single entry containing EX (Co-ab) and chained EX (CCA) of a character."""

    ex_ability_data: ExAbilityData
    cex_ability_data: ChainedExAbilityData

    def to_json_entry(self) -> dict[str, Any]:
        # Effect units are sorted by the condition to guarantee the atomicity
        return {
            "chara": super().to_json_entry(),
            "ex": [
                AbilityVariantEffectEntry(self.asset_manager, effect_unit).to_json_entry()
                for effect_unit in sorted(self.ex_ability_data.effect_units, key=lambda unit: unit.condition_comp)
            ],
            "chainedEx": [
                AbilityVariantEffectEntry(self.asset_manager, effect_unit).to_json_entry()
                for effect_unit in sorted(self.cex_ability_data.effect_units, key=lambda unit: unit.condition_comp)
            ],
        }
