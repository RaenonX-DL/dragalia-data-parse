"""Classes for ability variant data."""
from dlparse.enums import ConditionComposite
from dlparse.mono.asset import AbilityEntry

from .ability_var_common import AbilityVariantEffectPayload

__all__ = ("make_payload_ability",)


def make_payload_ability(ability_entry: AbilityEntry) -> AbilityVariantEffectPayload:
    """Make the payload for parsing the ability variant from ``ability_entry``."""
    condition_comp: ConditionComposite = ConditionComposite()

    # Get the on-skill conditions
    if on_skill_cond := ability_entry.on_skill_condition:
        condition_comp += on_skill_cond

    # Delay the determination of the ability variant effect condition
    # if the ability condition type relates to "shapeshifted to dragon"
    if not ability_entry.condition.condition_type.is_shapeshifted_to_dragon:
        # If the ability does not have condition, skip adding it
        if ability_cond := ability_entry.condition.to_condition_comp():
            condition_comp += ability_cond

    # Get the condition information
    cooldown_sec = ability_entry.condition.cooldown_sec
    max_occurrences = ability_entry.condition.max_occurrences

    # Get the variant payload
    return AbilityVariantEffectPayload(
        condition_comp=condition_comp,
        condition_cooldown=cooldown_sec,
        source_ability=ability_entry,
        max_occurrences=max_occurrences,
    )
