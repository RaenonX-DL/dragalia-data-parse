"""Base classes of an effect unit."""
from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import Any, TypeVar

from dlparse.model import EffectUnitBase
from dlparse.mono.manager import AssetManager
from .entry import JsonExportableEntryBase
from .text import TextEntry

__all__ = ("EffectUnitEntryBase",)

T = TypeVar("T", bound=EffectUnitBase)


@dataclass
class EffectUnitEntryBase(JsonExportableEntryBase, ABC):
    """Base class of an effect unit entry."""

    asset_manager: InitVar[AssetManager]

    effect_unit: T

    status_trans: TextEntry = field(init=False)
    target_trans: TextEntry = field(init=False)
    buff_param_trans: TextEntry = field(init=False)

    def __post_init__(self, asset_manager: AssetManager):
        self.status_trans = TextEntry(
            asset_text_website=asset_manager.asset_text_website, labels=self.effect_unit.status.translation_id,
            asset_text_multi=asset_manager.asset_text_multi
        )
        self.target_trans = TextEntry(
            asset_text_website=asset_manager.asset_text_website, labels=self.effect_unit.target.translation_id,
            asset_text_multi=asset_manager.asset_text_multi
        )
        self.buff_param_trans = TextEntry(
            asset_text_website=asset_manager.asset_text_website, labels=self.effect_unit.parameter.translation_id,
            asset_text_multi=asset_manager.asset_text_multi
        )

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "status": self.status_trans.to_json_entry(),
            "target": self.target_trans.to_json_entry(),
            "parameter": {
                "name": self.buff_param_trans.to_json_entry(),
                "code": self.effect_unit.parameter.value,
            },
            "probabilityPct": self.effect_unit.probability_pct,
            "rate": self.effect_unit.rate,
            "slipInterval": self.effect_unit.slip_interval,
            "slipDamageMod": self.effect_unit.slip_damage_mod,
            "durationSec": self.effect_unit.duration_sec,
            "durationCount": self.effect_unit.duration_count,
            "maxStackCount": self.effect_unit.max_stack_count,
            "stackable": self.effect_unit.stackable
        }
