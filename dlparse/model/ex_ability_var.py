"""Classes for ability variant data."""
from dlparse.enums import ConditionComposite
from dlparse.mono.asset import ExAbilityEntry

from .ability_var_common import AbilityVariantEffectPayload

__all__ = ("make_payload_ex_ability",)


def make_payload_ex_ability(ex_ability_entry: ExAbilityEntry) -> AbilityVariantEffectPayload:
    """Make the payload for parsing the ability variant from ``ex_ability_entry``."""
    condition_comp: ConditionComposite = ConditionComposite()

    # If the ability does not have condition, skip adding it
    if ability_cond := ex_ability_entry.condition.to_condition_comp():
        condition_comp += ability_cond

    # Get the variant payload
    return AbilityVariantEffectPayload(
        condition_comp=condition_comp,
        condition_cooldown=0,
        source_ability=ex_ability_entry,
        max_occurrences=1,  # an EX can exist in a team at most once
    )
