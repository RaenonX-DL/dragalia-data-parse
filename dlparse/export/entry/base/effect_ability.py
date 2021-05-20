"""Base classes of an ability effect unit."""
from dataclasses import dataclass, field
from typing import Any

from dlparse.model import AbilityVariantEffectUnit
from dlparse.mono.manager import AssetManager
from .effect import EffectUnitEntryBase
from .text import TextEntry

__all__ = ("AbilityVariantEffectEntry",)


@dataclass
class AbilityVariantEffectEntry(EffectUnitEntryBase):
    """Ability variant effect unit entry."""

    effect_unit: AbilityVariantEffectUnit

    target_action_trans: TextEntry = field(init=False)

    def __post_init__(self, asset_manager: AssetManager):
        super().__post_init__(asset_manager)

        self.target_action_trans = TextEntry(
            asset_manager.asset_text_website, self.effect_unit.target_action.translation_id
        )

    def to_json_entry(self) -> dict[str, Any]:
        ret = super().to_json_entry()

        ret.update({
            "sourceAbilityId": self.effect_unit.source_ability_id,
            "conditions": [condition.value for condition in self.effect_unit.condition_comp.conditions_sorted],
            "cooldownSec": self.effect_unit.cooldown_sec,
            "maxOccurrences": self.effect_unit.max_occurrences,
            "rateMax": self.effect_unit.rate_max,
            "targetAction": self.target_action_trans.to_json_entry()
        })

        return ret
