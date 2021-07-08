"""Models for a normal attack info chain."""
from dataclasses import InitVar, dataclass, field
from typing import Optional, TYPE_CHECKING

from dlparse.enums import ConditionComposite, SkillCancelType
from .unit_cancel import SkillCancelActionUnit

if TYPE_CHECKING:
    from dlparse.mono.asset import PlayerActionPrefab, HitAttrEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("NormalAttackChain", "NormalAttackCombo")


@dataclass
class NormalAttackComboBranch:
    """A branch of a normal attack combo info."""

    conditions: ConditionComposite

    hit_labels: list[str] = field(default_factory=list)
    mods: list[float] = field(default_factory=list)
    od_rate: list[float] = field(default_factory=list)
    crisis_mod: list[float] = field(default_factory=list)
    sp_gain: int = field(default=0)
    utp_gain: int = field(default=0)

    def fill_info_from_hit_attr(self, hit_attr: "HitAttrEntry"):
        """Fill the info of ``hit_attr`` into this combo branch."""
        self.hit_labels.append(hit_attr.id)
        self.mods.append(hit_attr.damage_modifier)
        self.crisis_mod.append(hit_attr.rate_boost_on_crisis)
        self.od_rate.append(hit_attr.rate_boost_in_od)

        # Both SP and UTP recovers on the initial hit only
        if not self.sp_gain:
            self.sp_gain = hit_attr.on_hit_sp_regen
        if not self.utp_gain:
            self.utp_gain += hit_attr.on_hit_utp_regen


@dataclass
class NormalAttackCombo:
    """Class for a single combo in a normal attack chain."""

    asset_manager: "AssetManager"
    action_prefab: "PlayerActionPrefab"

    level: InitVar[Optional[int]] = None

    cancel_actions: list[SkillCancelActionUnit] = field(init=False)

    combo_info: dict[ConditionComposite, NormalAttackComboBranch] = field(init=False)

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
        self.combo_info = {}

        for hit_attr_label, action_component in self.action_prefab.get_hit_actions(level):
            hit_attr = self.asset_manager.asset_hit_attr.get_data_by_id(hit_attr_label)

            if not hit_attr.is_effective_to_enemy(True):
                continue  # Dummy hit attribute might be inserted for...animation? (Nino `SWD_NIN_BLT_01_H00`)

            # Create one if not available yet
            conditions = ConditionComposite(action_component.skill_pre_condition)
            if conditions not in self.combo_info:
                self.combo_info[conditions] = NormalAttackComboBranch(conditions)

            # Fill hit attr info
            self.combo_info[conditions].fill_info_from_hit_attr(hit_attr)

    def __post_init__(self, level: Optional[int] = None):
        self.cancel_actions = SkillCancelActionUnit.from_player_action_prefab(self.action_prefab)
        self._init_next_combo_action_id()
        self._init_combo_props(level)


@dataclass
class NormalAttackChain:
    """Class for a normal attack chain."""

    combos: list[NormalAttackCombo]
