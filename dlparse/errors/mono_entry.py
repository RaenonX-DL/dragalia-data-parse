"""Mono behavior entry error classes."""
from typing import Optional

from .base import EntryNotFoundError

__all__ = ("SkillDataNotFoundError", "ActionDataNotFoundError", "TextLabelNotFoundError")


class SkillDataNotFoundError(EntryNotFoundError):
    """Error to be raised if the skill data is not found."""

    def __init__(self, skill_id: int):
        super().__init__(f"Skill data of ID `{skill_id}` not found")

        self._skill_id = skill_id

    @property
    def skill_id(self):
        """Get the skill ID that causes this error."""
        return self._skill_id


class ActionDataNotFoundError(EntryNotFoundError):
    """Error to be raised if the action data file is not found."""

    def __init__(self, action_id: int, skill_id: Optional[int] = None):
        super().__init__(f"Action data of action ID `{action_id}` / skill ID `{skill_id}` not found")


class TextLabelNotFoundError(EntryNotFoundError):
    """Error to be raised if the text label is not found."""

    def __init__(self, label: str):
        super().__init__(f"Text of label {label} not found")
