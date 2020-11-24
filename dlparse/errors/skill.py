"""Errors related to skill parsing / transforming."""
from abc import ABC

from .base import AppValueError

__all__ = ("ConditionValidationFailedError", "BulletEndOfLifeError", "DamagingHitValidationFailedError")


class ConditionValidationFailedError(AppValueError):
    """Error to be raised if the given condition combination is invalid."""

    def __init__(self, result):
        super().__init__(f"Skill combination validation failed. Reason: {result}")

        self._result = result

    @property
    def result(self):
        """Get the validation result that causes this error."""
        return self._result


class DamagingHitValidationFailedError(AppValueError):
    """Error to be raised if the initialization of a damaging hit failed."""


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
