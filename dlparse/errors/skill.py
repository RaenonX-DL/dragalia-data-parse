"""Errors related to skill parsing / transforming."""
from .base import AppValueError

__all__ = ("ConditionValidationFailedError",)


class ConditionValidationFailedError(AppValueError):
    """Error to be raised if the given condition combination is invalid."""

    def __init__(self, result):
        super().__init__(f"Skill combination validation failed. Reason: {result}")

        self._result = result

    @property
    def result(self):
        """Get the validation result that causes this error."""
        return self._result
