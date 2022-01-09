"""Enums of the color themes available on the website."""
from enum import Enum

__all__ = ("ColorTheme",)


class ColorTheme(str, Enum):
    """Color themes available on the website in enums."""

    # Bootstrap built-in
    PRIMARY = "dark-primary"
    SECONDARY = "secondary"
    SUCCESS = "dark-success"
    DANGER = "dark-danger"
    WARNING = "dark-warning"
    INFO = "dark-info"

    # Custom
    ORANGE = "dark-orange"

    @classmethod
    def get_all_available_themes(cls) -> list[str]:
        """Get all available color themes."""
        # noinspection PyUnresolvedReferences
        return [enum.value for enum in cls]
