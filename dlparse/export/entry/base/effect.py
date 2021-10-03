"""Base classes of an effect unit."""
from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import Any, TypeVar

from dlparse.enums import get_image_path
from dlparse.model import EffectUnitBase
from dlparse.mono.manager import AssetManager
from .entry import JsonExportableEntryBase
from .text import TextEntry
from .type import JsonSchema

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
    buff_unit_trans: TextEntry = field(init=False)

    def __post_init__(self, asset_manager: AssetManager):
        self.status_trans = TextEntry(
            asset_text_base=asset_manager.asset_text_website, labels=self.effect_unit.status.translation_id,
            asset_text_additional=asset_manager.asset_text_multi
        )
        self.target_trans = TextEntry(
            asset_text_base=asset_manager.asset_text_website, labels=self.effect_unit.target.translation_id,
            asset_text_additional=asset_manager.asset_text_multi
        )
        self.buff_param_trans = TextEntry(
            asset_text_base=asset_manager.asset_text_website, labels=self.effect_unit.parameter.translation_id,
            asset_text_additional=asset_manager.asset_text_multi
        )
        self.buff_unit_trans = TextEntry(
            asset_text_base=asset_manager.asset_text_website,
            asset_text_additional=asset_manager.asset_text_multi,
            labels=self.effect_unit.parameter.parameter_unit.translation_id
        )

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "status": TextEntry.json_schema,
            "target": TextEntry.json_schema,
            "parameter": {
                "name": TextEntry.json_schema,
                "code": int,
                "imagePath": str
            },
            "paramUnit": {
                "name": TextEntry.json_schema,
                "code": int,
                "isPercentage": bool
            },
            "probabilityPct": float,
            "rate": float,
            "slipInterval": float,
            "slipDamageMod": float,
            "durationSec": float,
            "durationCount": int,
            "maxStackCount": int,
            "stackable": bool
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "status": self.status_trans.to_json_entry(),
            "target": self.target_trans.to_json_entry(),
            "parameter": {
                "name": self.buff_param_trans.to_json_entry(),
                "code": self.effect_unit.parameter.value,
                "imagePath": get_image_path(self.effect_unit.parameter, on_not_found=None)
            },
            "paramUnit": {
                "name": self.buff_unit_trans.to_json_entry(),
                "code": self.effect_unit.parameter.parameter_unit.value,
                "isPercentage": self.effect_unit.parameter.is_value_percentage,
            },
            "probabilityPct": self.effect_unit.probability_pct,
            "rate": self.effect_unit.rate,
            "slipInterval": self.effect_unit.slip_interval_sec,
            "slipDamageMod": self.effect_unit.slip_damage_mod,
            "durationSec": self.effect_unit.duration_sec,
            "durationCount": self.effect_unit.duration_count,
            "maxStackCount": self.effect_unit.max_stack_count,
            "stackable": self.effect_unit.stackable
        }
