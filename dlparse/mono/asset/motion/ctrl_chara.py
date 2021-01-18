"""Motion controller classes for a character."""
from dataclasses import dataclass, field
from typing import Any

from dlparse.mono.asset.base import MotionControllerBase, get_file_like, get_file_path, parse_motion_data
from .clip import AnimationClipDataAnimatorOverrideController

__all__ = ("MotionControllerChara",)


@dataclass
class MotionControllerChara(MotionControllerBase):
    """Motion controller for a character."""

    # Init vars
    json_dict: dict[str, Any]

    # Parsed vars
    name: str = field(init=False)
    clip_override_path: dict[int, int] = field(init=False)  # K = original clip path ID, V = override clip path ID
    clip_stop_time: dict[int, float] = field(init=False)  # K = override clip path ID, V = override clip stop time

    def __post_init__(self):
        self.name = self.json_dict["$Name"]

        self.clip_override_path = {}
        self.clip_stop_time = {}
        for clip in self.json_dict["$Clips"]:
            clip = AnimationClipDataAnimatorOverrideController(clip)

            self.clip_override_path[clip.path_id_original] = clip.path_id_override
            self.clip_stop_time[clip.path_id_override] = clip.stop_time

    def is_clip_overridden(self, clip_id: int) -> bool:
        """Check if the animation clip of at ``clip_id`` is overridden."""
        return clip_id in self.clip_override_path

    def get_stop_time_by_original_clip_id(self, original_clip_id: int) -> float:
        """Get the animation stop time given ``original_clip_id``."""
        override_clip_id = self.clip_override_path[original_clip_id]
        return self.clip_stop_time[override_clip_id]

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
