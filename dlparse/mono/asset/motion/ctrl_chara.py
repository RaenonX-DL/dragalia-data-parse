"""Motion controller classes for a character."""
from dataclasses import dataclass
from typing import Any

from dlparse.mono.asset.base import get_file_like, get_file_path, parse_motion_data
from dlparse.mono.asset.extension import AnimatorOverrideController

__all__ = ("MotionControllerChara",)


@dataclass
class MotionControllerChara(AnimatorOverrideController):
    """``AnimatorOverrideController`` of a character."""

    # Init vars
    json_dict: dict[str, Any]

    @staticmethod
    def parse_raw(data: dict[str, Any]) -> "MotionControllerChara":
        return MotionControllerChara(data)

    @staticmethod
    def load_from_file(file_dir: str, file_path: str) -> "MotionControllerChara":
        """
        Load the character motion controller from a file.

        ``file_path`` should **NOT** contain ``file_dir``.
        """
        file_like = get_file_like(get_file_path(file_path, asset_dir=file_dir))

        return MotionControllerChara.parse_raw(parse_motion_data(file_like))
