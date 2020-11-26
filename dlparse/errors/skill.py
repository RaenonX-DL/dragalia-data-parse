"""Errors related to skill parsing / transforming."""
from abc import ABC

from .base import AppValueError

__all__ = ("ConditionValidationFailedError", "BulletEndOfLifeError", "DamagingHitValidationFailedError",
           "HitDataUnavailableError")


class ConditionValidationFailedError(AppValueError):
    """Error to be raised if the given condition combination is invalid."""

    def __init__(self, result):
        super().__init__(f"Skill condition validation failed. Check result: {result}")


class DamagingHitValidationFailedError(AppValueError):
    """Error to be raised if the initialization of a damaging hit failed."""


class HitDataUnavailableError(AppValueError):
    """Error to be raised if no hit data is available."""

    def __init__(self):
        super().__init__("No hit data available. This is likely due to a wrong skill type choice. "
                         "For example, a supportive skill transformed as an attacking skill.")


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
