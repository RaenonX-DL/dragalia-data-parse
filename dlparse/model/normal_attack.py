"""Models for a normal attack info chain."""
from dataclasses import InitVar, dataclass, field
from typing import Optional, TYPE_CHECKING

from dlparse.enums import SkillCancelType
from .unit_cancel import SkillCancelActionUnit

if TYPE_CHECKING:
    from dlparse.mono.asset import PlayerActionPrefab
    from dlparse.mono.manager import AssetManager

__all__ = ("NormalAttackChain", "NormalAttackCombo")


@dataclass
class NormalAttackCombo:
    """Class for a single combo in a normal attack chain."""

    asset_manager: "AssetManager"
    action_prefab: "PlayerActionPrefab"

    level: InitVar[Optional[int]] = None

    cancel_actions: list[SkillCancelActionUnit] = field(init=False)

    hit_labels: list[str] = field(init=False)
    mods: list[float] = field(init=False)
    od_rate: list[float] = field(init=False)
    crisis_mod: list[float] = field(init=False)
    sp_gain: int = field(init=False)
    utp_gain: int = field(init=False)

    next_combo_action_id: Optional[int] = field(init=False)

    def _init_next_combo_action_id(self):
        for cancel_action in self.cancel_actions:
            if cancel_action.cancel_type != SkillCancelType.NONE or cancel_action.action.is_common_action:
                # - Next combo action type should be `NONE`; things like `FS` should be excluded
                # - Excludes common actions (such as roll dodge)
                #   - legacy actions does not have cancel type assigned
                continue

            if not cancel_action.action_id:
                continue  # Action ID = 0 means any action, definitely not the next combo

            self.next_combo_action_id = cancel_action.action_id
            return

        self.next_combo_action_id = None

    def _init_combo_props(self, level: int):
        self.hit_labels = []
        self.mods = []
        self.crisis_mod = []
        self.od_rate = []
        self.sp_gain = 0
        self.utp_gain = 0

        for hit_attr_label, _ in self.action_prefab.get_hit_actions(level):
            hit_attr = self.asset_manager.asset_hit_attr.get_data_by_id(hit_attr_label)

            if not hit_attr.is_effective_to_enemy(True):
                continue  # Dummy hit attribute might be inserted for...animation? (Nino `SWD_NIN_BLT_01_H00`)

            self.hit_labels.append(hit_attr_label)
            self.mods.append(hit_attr.damage_modifier)
            self.crisis_mod.append(hit_attr.rate_boost_on_crisis)
            self.od_rate.append(hit_attr.rate_boost_in_od)

            # Both SP and UTP recovers on the initial hit only
            if not self.sp_gain:
                self.sp_gain = hit_attr.on_hit_sp_regen
            if not self.utp_gain:
                self.utp_gain += hit_attr.on_hit_utp_regen

    def __post_init__(self, level: Optional[int] = None):
        self.cancel_actions = SkillCancelActionUnit.from_player_action_prefab(self.action_prefab)
        self._init_next_combo_action_id()
        self._init_combo_props(level)


@dataclass
class NormalAttackChain:
    """Class for a normal attack chain."""

    combos: list[NormalAttackCombo]
