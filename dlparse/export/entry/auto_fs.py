"""Normal attack chain info data entry."""
from dataclasses import InitVar, dataclass, field
from typing import Any, TYPE_CHECKING

from dlparse.enums import ConditionComposite
from dlparse.model import AutoFsChain as AutoFsChainModel, NormalAttackComboBranch
from .base import JsonExportableEntryBase, JsonSchema, SkillCancelInfoEntry, TextEntry

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("AutoFsChain", "AutoFsChainEntry")


@dataclass
class AttackFsComboEntry(JsonExportableEntryBase):
    """A single entry representing a normal attack/FS combo."""

    combo: NormalAttackComboBranch

    cancel_actions: list[SkillCancelInfoEntry] = field(init=False)

    def __post_init__(self):
        self.cancel_actions = [SkillCancelInfoEntry(cancel_action) for cancel_action in self.combo.cancel_actions]

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "cancelActions": [SkillCancelInfoEntry.json_schema],
            "cancelToNextSec": [float, None],
            "mods": [float],
            "odRate": [float],
            "crisisMod": [float],
            "sp": int,
            "utp": int,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "cancelActions": [cancel_action.to_json_entry() for cancel_action in self.cancel_actions],
            "cancelToNextSec": self.combo.cancel_to_next_action_sec,
            "mods": self.combo.mods,
            "odRate": self.combo.od_rate,
            "crisisMod": self.combo.crisis_mod,
            "sp": self.combo.sp_gain,
            "utp": self.combo.utp_gain,
        }


@dataclass
class AutoFsBranchedChainEntry(JsonExportableEntryBase):
    """A single entry representing a branched normal attack/FS chain."""

    branched_combos: InitVar[list[NormalAttackComboBranch]]
    conditions: ConditionComposite

    combos: list[AttackFsComboEntry] = field(init=False)

    has_utp: bool = field(init=False)
    has_crisis_mods: bool = field(init=False)

    def __post_init__(self, branched_combos: list[NormalAttackComboBranch]):
        self.combos = [AttackFsComboEntry(combo) for combo in branched_combos]
        self.has_utp = any(combo.utp_gain > 0 for combo in branched_combos)
        self.has_crisis_mods = any(any(combo.crisis_mod) for combo in branched_combos)

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "conditions": [int],
            "combos": [AttackFsComboEntry.json_schema],
            "hasUtp": bool,
            "hasCrisis": bool,
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "conditions": [condition.value for condition in self.conditions.conditions_sorted],
            "combos": self.combos,
            "hasUtp": self.has_utp,
            "hasCrisis": self.has_crisis_mods,
        }


@dataclass
class AutoFsChainEntry(JsonExportableEntryBase):
    """A single entry representing a normal attack/FS chain."""

    asset_manager: "AssetManager"

    source_mode_id: InitVar[int]  # `0` for default; `-1` for unique dragon
    chain: InitVar[AutoFsChainModel]

    chain_name: TextEntry = field(init=False)
    chain_branches: list[AutoFsBranchedChainEntry] = field(init=False)

    def __post_init__(self, source_mode_id: int, chain: AutoFsChainModel):
        self.chain_name = TextEntry(
            self.asset_manager.asset_text_website,
            f"NORMAL_ATTACK_COMBO_CHAIN_{source_mode_id}"
        )
        self.chain_branches = [
            AutoFsBranchedChainEntry(chain.with_condition(conditions), conditions)
            for conditions in chain.possible_conditions
        ]

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "chainName": TextEntry.json_schema,
            "chain": [AutoFsBranchedChainEntry.json_schema],
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "chainName": self.chain_name.to_json_entry(),
            "chain": self.chain_branches,
        }


@dataclass
class AutoFsChain(JsonExportableEntryBase):
    """A class representing the normal attack and the FS chain."""

    asset_manager: "AssetManager"

    fs_chains: list[AutoFsChainEntry]
    normal_chains: list[AutoFsChainEntry]

    @classmethod
    @property
    def json_schema(cls) -> JsonSchema:
        return {
            "fs": [AutoFsChainEntry.json_schema],
            "auto": [AutoFsChainEntry.json_schema],
        }

    def to_json_entry(self) -> dict[str, Any]:
        return {
            "fs": [chain.to_json_entry() for chain in self.fs_chains],
            "auto": [chain.to_json_entry() for chain in self.normal_chains],
        }
