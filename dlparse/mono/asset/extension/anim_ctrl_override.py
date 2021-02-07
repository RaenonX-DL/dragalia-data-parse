"""Interface for an ``AnimatorOverrideController.``"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from dlparse.mono.asset.base import AnimationControllerBase, EntryBase

__all__ = ("AnimatorOverrideController",)


@dataclass
class AnimationClipDataAnimatorOverrideController:
    """Class for the animation clip data in an ``AnimatorOverrideController``."""

    json_dict: dict[str, Any]

    path_id_original: int = field(init=False)
    path_id_override: int = field(init=False)
    name: str = field(init=False)
    stop_time: float = field(init=False)

    def __post_init__(self):
        self.path_id_original = self.json_dict["$OriginalClip"]["m_PathID"]
        self.path_id_override = self.json_dict["$OverrideClip"]["m_PathID"]
        self.name = self.json_dict["$Name"]
        self.stop_time = self.json_dict["$StopTime"]


class AnimatorOverrideController(AnimationControllerBase, EntryBase, ABC):
    """
    Base class of an ``AnimatorOverrideController``.

    .. note::
        A controller selects the animation clip to use for a certain motion.
        The animation clip may be overridden by calling
        an ``AnimatorController`` and an ``AnimatorOverrideController`` at the same time.
    """

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
    @abstractmethod
    def parse_raw(data: dict[str, Any]) -> "AnimatorOverrideController":
        """Parse a raw data entry to an ``AnimatorOverrideController``."""
        raise NotImplementedError()
