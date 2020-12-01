"""Errors related to skill parsing / transforming."""
from abc import ABC
from typing import Any

from .base import AppValueError

__all__ = ("ConditionValidationFailedError", "BulletEndOfLifeError", "DamagingHitValidationFailedError",
           "HitDataUnavailableError", "UnhandledSelfDamageError", "InvalidSkillNumError")


class ConditionValidationFailedError(AppValueError):
    """Error to be raised if the given condition combination is invalid."""

    def __init__(self, result, additional: Any = None):
        super().__init__(f"Skill condition validation failed. Check result: {result} - {additional}")


class DamagingHitValidationFailedError(AppValueError):
    """Error to be raised if the initialization of a damaging hit failed."""


class HitDataUnavailableError(AppValueError):
    """Error to be raised if no hit data is available."""

    def __init__(self):
        super().__init__("No hit data available. This is likely due to a wrong skill type choice. "
                         "For example, a supportive skill transformed as an attacking skill.")


class UnhandledSelfDamageError(AppValueError):
    """Error to be raised if the self damaging skill is unhandled."""

    def __init__(self, hit_attr_id: str):
        super().__init__(f"Unhandled self damage at hit attribute `{hit_attr_id}`")


class InvalidSkillNumError(AppValueError):
    """Error to be raised if the given skill number is invalid."""

    def __init__(self, skill_num: int):
        super().__init__(f"Skill number `{skill_num}` is invalid")


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
