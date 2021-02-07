"""Enums of the color themes available on the website."""
from enum import Enum

__all__ = ("ColorTheme",)


class ColorTheme(str, Enum):
    """Color themes available on the website in enums."""

    # Bootstrap built-in
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"

    # Custom
    OM_DARK = "om-dark"
    OM_LIGHT = "om-light"
    SKYBLUE_LIGHT = "skyblue-light"
    DARK_RED = "dark-red"
    BLACK_32 = "black-32"
    BLACK_50 = "black-50"
    ORANGE = "orange"

    @classmethod
    def get_all_available_themes(cls) -> list[str]:
        """Get all available color themes."""
        # noinspection PyUnresolvedReferences
        return [enum.value for enum in cls]
