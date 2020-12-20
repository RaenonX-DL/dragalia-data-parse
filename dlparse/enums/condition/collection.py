"""Condition enum collections."""
from .items import Condition

__all__ = ("cond_afflictions", "cond_elements")

# Conditions that are only a collection without the needs of any other functionalities should be placed here,
# instead of :class:`ConditionCategories`.
# All collections should be prefixed with `cond_`.


# Used for target affliction condition on the website
cond_afflictions: tuple[Condition, ...] = (
    Condition.TARGET_POISONED,
    Condition.TARGET_BURNED,
    Condition.TARGET_FROZEN,
    Condition.TARGET_PARALYZED,
    Condition.TARGET_BLINDED,
    Condition.TARGET_STUNNED,
    Condition.TARGET_CURSED,
    Condition.TARGET_BOGGED,
    Condition.TARGET_SLEPT,
    Condition.TARGET_FROSTBITTEN,
    Condition.TARGET_FLASHBURNED,
    Condition.TARGET_STORMLASHED,
    Condition.TARGET_SHADOWBLIGHTED,
    Condition.TARGET_SCORCHRENT,
)

# Used for target element on the website
cond_elements: tuple[Condition, ...] = (
    Condition.TARGET_ELEM_FLAME,
    Condition.TARGET_ELEM_WATER,
    Condition.TARGET_ELEM_WIND,
    Condition.TARGET_ELEM_LIGHT,
    Condition.TARGET_ELEM_SHADOW,
    Condition.TARGET_ELEM_WEAK,
    Condition.TARGET_ELEM_EFFECTIVE,
)
