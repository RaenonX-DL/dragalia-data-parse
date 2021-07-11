"""Models for a normal attack info chain."""
from dataclasses import InitVar, dataclass, field
from typing import Iterable, Optional, TYPE_CHECKING

from dlparse.enums import Condition, ConditionComposite, SkillCancelType
from .unit_cancel import SkillCancelActionUnit

if TYPE_CHECKING:
    from dlparse.mono.asset import PlayerActionPrefab, HitAttrEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("NormalAttackChain", "NormalAttackCombo", "NormalAttackComboBranch")

PRE_CONDITIONS_TO_OMIT: set[Condition] = {
    Condition.SELF_GMASCULA_S1_LV1,
    Condition.SELF_GMASCULA_S1_LV2
}

# - Faris (10950102) root normal attack action (901000) have action cancel component goes to `901201`.
#   However, such action does not exist. (Should be `901001` instead).
# --------------------
# No manual fix because it won't reflect the actual game playing data,
# despite the action may exist, such as `901001` as mentioned above.
MISSING_ACTION_IDS: set[int] = {901201}


@dataclass
class NormalAttackComboBranch:
    """A branch of a normal attack combo info."""

    conditions: ConditionComposite

    cancel_actions: list[SkillCancelActionUnit]

    next_action_id: InitVar[int]

    hit_labels: list[str] = field(default_factory=list)
    mods: list[float] = field(default_factory=list)
    od_rate: list[float] = field(default_factory=list)
    crisis_mod: list[float] = field(default_factory=list)
    sp_gain: int = field(default=0)
    utp_gain: int = field(default=0)

    cancel_to_next_action_sec: Optional[float] = field(init=False)

    def __post_init__(self, next_action_id: int):
        self.cancel_to_next_action_sec = next(
            (
                cancel_action.time for cancel_action in self.cancel_actions
                if cancel_action.action_id == next_action_id
            ),
            None
        )

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

            if cancel_action.time == 0:
                continue  # Next combo should not be able to change immediately

            if cancel_action.action_id in MISSING_ACTION_IDS:
                continue  # Check the notes for `MISSING_ACTION_IDS`

            self.next_combo_action_id = cancel_action.action_id
            return

        self.next_combo_action_id = None

    def _init_fill_combo_info(self, condition_list: Iterable[ConditionComposite], hit_attr: "HitAttrEntry"):
        for conditions in condition_list:
            if conditions not in self.combo_info:
                self.combo_info[conditions] = NormalAttackComboBranch(
                    conditions, self.cancel_actions, self.next_combo_action_id
                )

            self.combo_info[conditions].fill_info_from_hit_attr(hit_attr)

    def _init_combo_props(self, level: int):
        self.combo_info = {}

        # Get all possible pre-conditions
        pre_conditions: set[ConditionComposite] = {
            ConditionComposite(action_component.skill_pre_condition)
            for _, action_component in
            self.action_prefab.get_hit_actions(level)
            if action_component.skill_pre_condition not in PRE_CONDITIONS_TO_OMIT
        }

        for hit_attr_label, action_component in self.action_prefab.get_hit_actions(level):
            hit_attr = self.asset_manager.asset_hit_attr.get_data_by_id(hit_attr_label)

            if not hit_attr.is_effective_to_enemy(True):
                continue  # Dummy hit attribute might be inserted for...animation? (Nino `SWD_NIN_BLT_01_H00`)

            if action_component.skill_pre_condition in PRE_CONDITIONS_TO_OMIT:
                continue  # Specific pre-conditions to omit

            # Get pre-conditions to fill combo info
            target_conditions: set[ConditionComposite] = (
                {ConditionComposite(action_component.skill_pre_condition)}
                if action_component.skill_pre_condition
                else pre_conditions
            )

            # Fill hit attr info
            self._init_fill_combo_info(target_conditions, hit_attr)

    def __post_init__(self, level: Optional[int] = None):
        self.cancel_actions = SkillCancelActionUnit.from_player_action_prefab(self.action_prefab)
        self._init_next_combo_action_id()
        self._init_combo_props(level)


@dataclass
class NormalAttackChain:
    """Class for a normal attack chain."""

    combos: list[NormalAttackCombo]

    possible_conditions: list[ConditionComposite] = field(init=False)

    def __post_init__(self):
        conditions = set()
        for combo in self.combos:
            conditions.update(combo.combo_info.keys())

        self.possible_conditions = list(sorted(conditions))

    def with_condition(self, conditions: ConditionComposite = ConditionComposite()) -> list[NormalAttackComboBranch]:
        """
        Get all combo info of a branch under ``conditions``.

        The order of the return is the same as ``combos``.
        """
        return [
            combo.combo_info[conditions]
            for combo in self.combos
            if conditions in combo.combo_info
        ]
