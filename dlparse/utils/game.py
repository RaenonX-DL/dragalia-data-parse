"""Functions for mimicking the in-game computations."""
from typing import Optional, TYPE_CHECKING
from warnings import warn

from dlparse.enums import SkillConditionCategories, SkillConditionComposite
from dlparse.mono.asset import ActionBullet, PlayerActionInfoAsset
from .calc import multiply_vector

if TYPE_CHECKING:
    from dlparse.model import DamagingHitData

__all__ = ("calculate_damage_modifier", "calculate_crisis_mod")


def calculate_crisis_mod(mod: float, hp_rate: float, crisis_rate: float) -> float:
    """
    Calculate the ``mod``, which correlates to ``crisis_rate``, at ``hp_rate``.

    In short, this is quadratic.
    """
    return mod * ((1 - hp_rate) ** 2 * (crisis_rate - 1) + 1)


def _calc_damage_mod_base(
        hit_data: "DamagingHitData", condition_comp: SkillConditionComposite, /,
        action_info_asset: Optional[PlayerActionInfoAsset] = None
) -> list[float]:
    hit_attr = hit_data.hit_attr

    if hit_data.will_deteriorate and condition_comp.bullet_hit_count:
        # Deteriorating bullets
        mods = [hit_data.damage_modifier_at_hit(hit_count)
                for hit_count in range(1, condition_comp.bullet_hit_count_converted + 1)]
    elif hit_data.is_effective_inside_buff_zone:
        # Damage mods inside buff zones i.e. no damage mod if not in buff zone
        mods = hit_data.mods_in_self_buff_zone(condition_comp.buff_zone_self_converted or 0)
        mods += hit_data.mods_in_ally_buff_zone(condition_comp.buff_zone_ally_converted or 0)
    elif hit_data.is_depends_on_user_buff_count:
        # Damage dealt depends on the user's buff count
        effective_buff_count: int = condition_comp.buff_count_converted or 0

        if action_info_asset:
            max_buff_hit_count = action_info_asset.get_data_by_id(hit_data.action_id).max_bullet_count
            effective_buff_count = min(max_buff_hit_count, effective_buff_count)
        else:
            warn(f"Max hits by user buff count unobtainable. Result might be inaccurate. "
                 f"(Hit attr ID: {hit_data.hit_attr.id})")

        mods = [hit_attr.damage_modifier] * effective_buff_count
    elif hit_data.is_depends_on_bullet_on_map:
        # Damage dealt depends on the bullets on the map
        mods = [hit_attr.damage_modifier] * (condition_comp.bullets_on_map_converted or 0)
    elif type(hit_data.action_component) is ActionBullet:  # pylint: disable=unidiomatic-typecheck
        # Action component is exactly `ActionPartsBullet`, max hit count may be in effect
        # For example, Lin You S1 (`104503011`, AID `491040` and `491042`)
        mods = [hit_attr.damage_modifier] * (hit_data.max_hit_count or 1)
    else:
        # Cases not handled above
        mods = [hit_attr.damage_modifier]

    return mods


def calculate_damage_modifier(
        hit_data: "DamagingHitData", condition_comp: SkillConditionComposite, /,
        action_info_asset: Optional[PlayerActionInfoAsset] = None
) -> list[float]:
    """
    Calculates the damage modifier of ``hit_data`` under ``condition_comp``.

    Usually, a single hit will have a single modifier.
    However, under some special circumstances (for example, deteriorating bullets),
    having multiple damage modifiers is possible.

    ``action_info_asset`` will be used for special circumstance mods calculation.
    If they are not provided, the mods may be uncalculatable or inaccurate.
    If such happens, an error will be raised, or a warning will be emitted.
    """
    # --- Early terminations / checks

    if hit_data.pre_condition:
        # Pre-condition available, perform checks

        if hit_data.pre_condition in SkillConditionCategories.skill_addl_inputs:
            # Pre-condition is additional inputs, perform special check
            pre_cond_addl_hit = SkillConditionCategories.skill_addl_inputs.convert(hit_data.pre_condition)
            if pre_cond_addl_hit > (condition_comp.addl_inputs_converted or 0):
                # Required pre-conditional additional inputs > additional inputs count in the condition, hit invalid
                return []
        elif hit_data.pre_condition not in condition_comp:
            # Other pre-conditions & not listed in the given condition composite i.e. pre-condition mismatch
            return []

    # --- Mod base

    mods = _calc_damage_mod_base(hit_data, condition_comp, action_info_asset=action_info_asset)

    # --- Apply boosts

    hit_attr = hit_data.hit_attr

    # HP boosts
    if hit_attr.boost_by_hp:
        mods = [calculate_crisis_mod(mod, condition_comp.hp_status_converted, hit_attr.rate_boost_on_crisis)
                for mod in mods]

    # Buff boosts
    if hit_attr.boost_by_buff_count and condition_comp.buff_count:
        mods = multiply_vector(mods, (1 + hit_attr.rate_boost_by_buff * condition_comp.buff_count_converted))

    # Punisher boosts
    if hit_attr.boost_on_target_afflicted and condition_comp.afflictions_converted & hit_attr.punisher_states:
        mods = multiply_vector(mods, hit_attr.punisher_rate)

    # Return non-zero mods only
    return [mod for mod in mods if mod]
