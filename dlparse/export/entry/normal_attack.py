"""Normal attack chain info data entry."""
from dataclasses import InitVar, dataclass, field
from typing import Any, TYPE_CHECKING

from dlparse.model import NormalAttackChain, NormalAttackCombo
from .base import JsonExportableEntryBase, JsonSchema, SkillCancelInfoEntry, TextEntry

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("NormalAttackChainEntry",)


@dataclass
class NormalAttackComboEntry(JsonExportableEntryBase):
    """A single entry representing a normal attack combo."""

    combo: NormalAttackCombo

    cancel_actions: list[SkillCancelInfoEntry] = field(init=False)

    def __post_init__(self):
        self.cancel_actions = [SkillCancelInfoEntry(cancel_action) for cancel_action in self.combo.cancel_actions]

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "cancelActions": [SkillCancelInfoEntry.json_schema],
            "mods": [float],
            "odRate": [float],
            "crisisMod": [float],
            "sp": int,
            "utp": int,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "cancelActions": [cancel_action.to_json_entry() for cancel_action in self.cancel_actions],
            "mods": self.combo.mods,
            "odRate": self.combo.od_rate,
            "crisisMod": self.combo.crisis_mod,
            "sp": self.combo.sp_gain,
            "utp": self.combo.utp_gain,
        }


@dataclass
class NormalAttackChainEntry(JsonExportableEntryBase):
    """A single entry representing a normal attack chain."""

    asset_manager: "AssetManager"

    source_mode_id: InitVar[int]  # `0` for default
    chain: InitVar[NormalAttackChain]

    chain_name: TextEntry = field(init=False)

    combos: list[NormalAttackComboEntry] = field(init=False)

    def __post_init__(self, source_mode_id: int, chain: NormalAttackChain):
        self.chain_name = TextEntry(
            self.asset_manager.asset_text_website,
            f"NORMAL_ATTACK_COMBO_CHAIN_{source_mode_id}"
        )
        self.combos = [NormalAttackComboEntry(combo) for combo in chain.combos]

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "combos": [NormalAttackComboEntry.json_schema],
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "combos": [combo.to_json_entry() for combo in self.combos],
        }
