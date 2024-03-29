"""Errors related to skill parsing / transforming."""
from abc import ABC
from typing import Any, TYPE_CHECKING, Union

from .base import AppValueError

if TYPE_CHECKING:
    from dlparse.enums import SkillNumber, Condition
    from dlparse.mono.asset import UnitEntry

__all__ = (
    "ConditionValidationFailedError", "BulletEndOfLifeError", "DamagingHitValidationFailedError",
    "HitDataUnavailableError", "ActionInfoNotFoundError", "InvalidSkillIdentifierLabelError",
    "UnhandledSelfDamageError", "InvalidSkillNumError", "InvalidSkillLevelError",
    "PreconditionCollidedError", "MultipleActionsError", "UnhandledUnitError"
)


class ConditionValidationFailedError(AppValueError):
    """Error to be raised if the given condition combination is invalid."""

    def __init__(self, result, additional: Any = None):
        super().__init__(f"Condition validation failed. Check result: {result} - {additional}")


class DamagingHitValidationFailedError(AppValueError):
    """Error to be raised if the initialization of a damaging hit failed."""


class HitDataUnavailableError(AppValueError):
    """Error to be raised if no hit data is available."""

    def __init__(self):
        super().__init__("No hit data available. This is likely due to a wrong skill type choice. "
                         "For example, a supportive skill transformed as an attacking skill.")


class ActionInfoNotFoundError(AppValueError):
    """Error to be raised if the corresponding action info is not found."""

    def __init__(self, action_id: int):
        super().__init__(f"Action info for AID `{action_id}` not found")


class UnhandledSelfDamageError(AppValueError):
    """Error to be raised if the self damaging skill is unhandled."""

    def __init__(self, hit_attr_id: str):
        super().__init__(f"Unhandled self damage at hit attribute `{hit_attr_id}`")


class InvalidSkillNumError(AppValueError):
    """Error to be raised if the given skill number is invalid."""

    def __init__(self, skill_num: Union["SkillNumber", int]):
        super().__init__(f"Skill number `{skill_num}` is invalid")


class InvalidSkillLevelError(AppValueError):
    """Error to be raised if the given skill level is invalid."""

    def __init__(self, skill_level: int):
        super().__init__(f"Skill level `{skill_level}` is invalid")


class InvalidSkillIdentifierLabelError(AppValueError):
    """Error to be raised if the parameters to generate the skill identifier label is invalid."""


class DamagaCalculationError(AppValueError, ABC):
    """Base class for the errors during damage calculation."""


class BulletEndOfLifeError(DamagaCalculationError):
    """
    Error to be raised if the bullet hit count is beyond the maximum possible hit count.

    For example, the bullets of Yukata Curran S1 can only have 6 hits at max,
    but the condition is requesting 7 bullet hits.
    """

    def __init__(self, lifetime_hit: int, hit_count: int):
        super().__init__(f"Bullet life ends (at hit {lifetime_hit}) before hitting {hit_count} times")


class PreconditionCollidedError(AppValueError):
    """Error to be raised if there are multiple pre-conditions available but not handled."""

    def __init__(self, pre_condition_1: "Condition", pre_condition_2: "Condition"):
        super().__init__(f"Multiple pre-conditions detected: {pre_condition_1} & {pre_condition_2}")


class MultipleActionsError(AppValueError):
    """Error to be raised if there are multiple actions sharing the same condition."""

    def __init__(self, action_id_mtx: list[set[int]]):
        super().__init__(f"Multiple actions sharing the same condition: {action_id_mtx}")

        self.action_id_mtx = action_id_mtx

    @property
    def all_possible_action_ids(self) -> set[int]:
        """Get all possible action IDs across levels."""
        return set(action_id for action_ids_lv in self.action_id_mtx for action_id in action_ids_lv)


class UnhandledUnitError(AppValueError):
    """Error to be raised if the unit type is unhandled."""

    def __init__(self, unit_entry: "UnitEntry"):
        super().__init__(f"Unhandled unit: ID #{unit_entry.id} / Type: {type(unit_entry)}")
