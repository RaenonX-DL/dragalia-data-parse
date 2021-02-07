"""Mono behavior entry error classes."""
from typing import Optional

from .base import AppValueError, EntryNotFoundError

__all__ = (
    "CharaDataNotFoundError", "NoUniqueDragonError", "SkillDataNotFoundError",
    "ActionDataNotFoundError", "MotionDataNotFoundError",
    "TextLabelNotFoundError",
    "AbilityLimitDataNotFoundError", "AbilityOnSkillUnconvertibleError", "LanguageAssetNotFoundError",
    "AbilityConditionUnconvertibleError", "BulletMaxCountUnavailableError", "AbilityVariantUnconvertibleError"
)


class CharaDataNotFoundError(EntryNotFoundError):
    """Error to be raised if the character data is not found."""

    def __init__(self, chara_id: int, message: str = ""):
        super().__init__(f"Character data of ID `{chara_id}` not found: {message}")


class NoUniqueDragonError(AppValueError):
    """Error to be raised if the character does not have an unique dragon while attempting to get its data."""

    def __init__(self, chara_id: int):
        super().__init__(f"No unique dragon binded to character #{chara_id}")


class SkillDataNotFoundError(EntryNotFoundError):
    """Error to be raised if the skill data is not found."""

    def __init__(self, skill_id: int):
        super().__init__(f"Skill data of ID `{skill_id}` not found")

        self._skill_id = skill_id

    @property
    def skill_id(self) -> int:
        """Get the skill ID that causes this error."""
        return self._skill_id


class MotionDataNotFoundError(EntryNotFoundError):
    """Error to be raised if the motion data file is not found."""

    def __init__(self, motion_name: str, message: str = ""):
        super().__init__(f"Motion data `{motion_name}` not found: {message}")


class ActionDataNotFoundError(EntryNotFoundError):
    """Error to be raised if the action data file is not found."""

    def __init__(self, action_id: int, skill_id: Optional[int] = None):
        super().__init__(f"Action data of action ID `{action_id}` / skill ID `{skill_id}` not found")


class LanguageAssetNotFoundError(EntryNotFoundError):
    """Error to be raised if the language asset is not found."""

    def __init__(self, lang_code: str):
        super().__init__(f"Language asset in code `{lang_code}` not found")


class TextLabelNotFoundError(EntryNotFoundError):
    """Error to be raised if the text label is not found."""

    def __init__(self, label: str):
        super().__init__(f"Text of label {label} not found")


class AbilityLimitDataNotFoundError(EntryNotFoundError):
    """Error to be raised if the ability limit data is not found."""

    def __init__(self, data_id: int):
        super().__init__(f"Ability limit data of ID {data_id} not found")


class AbilityVariantUnconvertibleError(AppValueError):
    """Error to be raised if the ability variant cannot be converted to ability variant effect unit."""

    def __init__(self, ability_id: int, variant_type: int, message: Optional[str] = None):
        super().__init__(
            f"Unable to convert ability variant to effect units "
            f"(ability ID: {ability_id} / variant type ID {variant_type}): {message or ''}"
        )


class AbilityConditionUnconvertibleError(AppValueError):
    """Error to be raised if the ability condition cannot be converted to condition."""

    def __init__(self, ability_condition: int, val_1: float, val_2: Optional[float] = None):
        super().__init__(f"Unable to convert ability condition to condition "
                         f"(ability condition code: {ability_condition} / val 1: {val_1} / val 2: {val_2})")


class AbilityOnSkillUnconvertibleError(AppValueError):
    """Error to be raised if the on skill field of the ability cannot be converted to condition."""

    def __init__(self, ability_id: int, on_skill: int):
        super().__init__(f"Unable to convert ability on skill condition to condition "
                         f"(ability ID: {ability_id} / on skill: {on_skill}")


class BulletMaxCountUnavailableError(AppValueError):
    """Error to be raised if the bullet max count cannot be obtained solely from its action component."""
