"""Functions for mimicking the in-game computations."""
from typing import TYPE_CHECKING

from dlparse.enums import SkillConditionComposite, SkillCondition
from .calc import multiply_vector

if TYPE_CHECKING:
    from dlparse.model import DamagingHitData

__all__ = ("calculate_damage_modifier",)


def calculate_damage_modifier(hit_data: "DamagingHitData", condition_comp: SkillConditionComposite) -> list[float]:
    """
    Calculates the damage modifier of ``hit_data`` under ``condition_comp``.

    Usually, a single hit will have a single modifier only.
    However, for deteriorating bullets, having multiple damage modifiers is possible.
    """
    hit_attr = hit_data.hit_attr

    # Create modifier bases
    if hit_data.will_deteriorate and condition_comp.bullet_hit_count:
        # Deteriorating bullets
        mods = [hit_data.damage_modifier_at_hit(hit_count)
                for hit_count in range(1, condition_comp.bullet_hit_count.to_bullet_hit_count() + 1)]
    else:
        # Normal cases
        mods = [hit_attr.damage_modifier]

    # --- Apply boosts

    # Crisis (low HP) boosts
    if hit_attr.boost_by_hp and condition_comp.hp_condition == SkillCondition.SELF_HP_1:
        mods = multiply_vector(mods, hit_attr.rate_boost_on_crisis)

    # Buff boosts
    if hit_attr.boost_by_buff_count and condition_comp.buff_count:
        mods = multiply_vector(mods, (1 + hit_attr.rate_boost_by_buff * condition_comp.buff_count.to_buff_count()))

    # Punisher boosts
    if hit_attr.boost_on_target_afflicted and condition_comp.afflictions_converted & hit_attr.punisher_states:
        mods = multiply_vector(mods, hit_attr.punisher_rate)

    return mods
