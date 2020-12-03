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
    # --- Early termination

    if hit_data.pre_condition and hit_data.pre_condition not in condition_comp:
        return []  # No damage mods because pre condition mismatched

    hit_attr = hit_data.hit_attr

    # --- Mod base

    # Create modifier bases
    if hit_data.will_deteriorate and condition_comp.bullet_hit_count:
        # Deteriorating bullets
        mods = [hit_data.damage_modifier_at_hit(hit_count)
                for hit_count in range(1, condition_comp.bullet_hit_count_converted + 1)]
    elif hit_data.is_effective_inside_buff_zone:
        # Damage mods inside buff zones i.e. no damage mod if not in buff zone
        mods = hit_data.mods_in_self_buff_zone(condition_comp.buff_zone_self_converted or 0)
        mods += hit_data.mods_in_ally_buff_zone(condition_comp.buff_zone_ally_converted or 0)
    else:
        # Normal cases
        mods = [hit_attr.damage_modifier]

    # --- Apply boosts

    # Crisis (low HP) boosts
    if hit_attr.boost_by_hp and condition_comp.hp_condition == SkillCondition.SELF_HP_1:
        mods = multiply_vector(mods, hit_attr.rate_boost_on_crisis)

    # Buff boosts
    if hit_attr.boost_by_buff_count and condition_comp.buff_count:
        mods = multiply_vector(mods, (1 + hit_attr.rate_boost_by_buff * condition_comp.buff_count_converted))

    # Punisher boosts
    if hit_attr.boost_on_target_afflicted and condition_comp.afflictions_converted & hit_attr.punisher_states:
        mods = multiply_vector(mods, hit_attr.punisher_rate)

    # Return non-zero mods only
    return [mod for mod in mods if mod]
