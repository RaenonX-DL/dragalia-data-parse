"""Buff count boost data model."""
from dataclasses import dataclass

from dlparse.enums import SkillConditionComposite
from dlparse.mono.asset import ActionConditionAsset, BuffCountAsset, HitAttrEntry

__all__ = ("BuffCountBoostData",)


@dataclass
class BuffCountBoostData:
    """Data used for calculating the damage boost according to the buff count."""

    in_effect_rate: float  # 0 = nothing in-effect
    """Rate of the buff boost already in-effect."""

    rate_limit: float  # 0 = unlimited
    """Maximum rate allowed."""
    rate_base: float  # 0 = no boost by buff count
    """Boost rate increase for each count of buffs."""

    action_condition_id: int  # 0 = not applicable
    """Action condition which has an enhanced boost rate."""
    action_condition_count_max: int  # 0 = uncapped
    """Maximum count of the action condition instances allowed."""
    action_condition_rate_each: float
    """Boost rate increase for each instance of the action condition."""

    @staticmethod
    def from_hit_attr(
            hit_attr: HitAttrEntry, condition_comp: SkillConditionComposite,
            asset_action_cond: ActionConditionAsset, asset_buff_count: BuffCountAsset
    ) -> "BuffCountBoostData":
        """Get the buff count boost data of ``hit_attr``."""
        if not hit_attr.boost_by_buff_count:
            return BuffCountBoostData(0, 0, 0, 0, 0, 0)  # Not boosted

        if hit_attr.rate_boost_by_buff:
            # Uncapped direct boost
            return BuffCountBoostData(
                hit_attr.rate_boost_by_buff * condition_comp.buff_count_converted,
                0,
                hit_attr.rate_boost_by_buff,
                0,
                0,
                0
            )

        # Capped buff count boost
        entry_buff_count = asset_buff_count.get_data_by_id(hit_attr.buff_boost_data_id)
        entry_action_cond = asset_action_cond.get_data_by_id(entry_buff_count.action_condition_id)
        action_cond_count = entry_buff_count.get_effective_action_condition_count(condition_comp)

        in_effect_rate = (action_cond_count * entry_buff_count.action_condition_rate
                          + condition_comp.buff_count_converted * entry_buff_count.rate_base)

        return BuffCountBoostData(
            min(in_effect_rate, entry_buff_count.rate_limit),
            entry_buff_count.rate_limit,
            entry_buff_count.rate_base,
            entry_buff_count.action_condition_id,
            entry_action_cond.max_instance_count - action_cond_count,
            entry_buff_count.action_condition_rate,
        )

    def __hash__(self):
        # x 1E5 for handling floating errors
        return hash((
            int(self.in_effect_rate * 1E5), int(self.rate_limit * 1E5), int(self.rate_base * 1E5),
            self.action_condition_id, self.action_condition_count_max, int(self.action_condition_rate_each * 1E5)
        ))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return hash(self) == hash(other)
