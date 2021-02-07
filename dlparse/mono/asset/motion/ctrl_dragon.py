"""Motion controller classes for a dragon."""
from dataclasses import dataclass
from typing import Any

from dlparse.mono.asset.base import get_file_like, get_file_path, parse_motion_data
from dlparse.mono.asset.extension import AnimatorController

__all__ = ("MotionControllerDragon",)


@dataclass
class MotionControllerDragon(AnimatorController):
    """Motion controller for a dragon."""

    # Init vars
    json_dict: dict[str, Any]

    @staticmethod
    def parse_raw(data: dict[str, Any]) -> "MotionControllerDragon":
        return MotionControllerDragon(data)

    @staticmethod
    def load_from_file(file_dir: str, file_path: str) -> "MotionControllerDragon":
        """
        Load the dragon motion controller from a file.

        ``file_path`` should **NOT** contain ``file_dir``.
        """
        file_like = get_file_like(get_file_path(file_path, asset_dir=file_dir))

        return MotionControllerDragon.parse_raw(parse_motion_data(file_like))
