"""Interface for an ``AnimatorController``."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, Union

from dlparse.errors import MotionDataNotFoundError
from dlparse.mono.asset.base import AnimationControllerBase, EntryBase
from .anim_ctrl_override import AnimatorOverrideController

__all__ = ("AnimatorController",)


@dataclass
class AnimationClipDataAnimatorController:
    """Class for the animation clip data in an ``AnimatorController``."""

    json_dict: dict[str, Any]

    path_id: int = field(init=False)
    name: str = field(init=False)
    stop_time: float = field(init=False)

    def __post_init__(self):
        self.path_id = self.json_dict["$PathID"]
        self.name = self.json_dict["$Name"]
        self.stop_time = self.json_dict["$StopTime"]


@dataclass
class AnimatorController(AnimationControllerBase, EntryBase, ABC):
    """Base class for an ``AnimatorController``."""

    # Init vars
    json_dict: dict[str, Any]

    # Parsed vars
    tos: dict[str, int] = field(init=False)  # K = motion name, V = state machine name ID
    state_machine_ref: dict[int, int] = field(init=False)  # K = state machine name ID, V = clip index (0-based)
    animation_clip_path_ids: list[int] = field(init=False)

    # --- K = animation clip ID, V = animation clip data
    animation_clips: dict[int, AnimationClipDataAnimatorController] = field(init=False)

    def __post_init__(self):
        controller = self.json_dict["$Controller"]
        clips = self.json_dict["$Clips"]

        self.tos = {}
        for tos in controller["m_TOS"]:
            self.tos[tos["Value"]] = tos["Key"]

        self.state_machine_ref = {}
        state_machine_array = controller["m_Controller"]["m_StateMachineArray"][0]["data"]["m_StateConstantArray"]
        for state_machine_data in state_machine_array:
            state_machine_data = state_machine_data["data"]

            name_id = state_machine_data["m_NameID"]
            clip_idx = state_machine_data["m_BlendTreeConstantArray"][0]["data"]["m_NodeArray"][0]["data"]["m_ClipID"]

            self.state_machine_ref[name_id] = clip_idx

        self.animation_clip_path_ids = []
        self.animation_clips = {}
        for animation_clip_pptr, clip in zip(controller["m_AnimationClips"], clips):
            clip_path_id: int = animation_clip_pptr["m_PathID"]

            self.animation_clip_path_ids.append(clip_path_id)
            self.animation_clips[clip_path_id] = AnimationClipDataAnimatorController(clip)

    def get_clip_id_by_motion_name(self, motion_name: str) -> int:
        """Get the animation clip ID given ``motion_name``."""
        state_name_id = self.tos[motion_name]
        clip_idx = self.state_machine_ref[state_name_id]
        return self.animation_clip_path_ids[clip_idx]

    def get_stop_time_by_clip_id(self, clip_path_id: int) -> float:
        """Get the animation stop time of the :class:`AnimationClip` at ``clip_path_id``."""
        return self.animation_clips[clip_path_id].stop_time

    def get_stop_time_by_motion_name(
            self, motion_name: str, override: Optional[AnimatorOverrideController] = None, /, error_msg: str = ""
    ) -> float:
        """
        Get the animation stop time of the :class:`AnimationClip` of motion named as ``motion_name``.

        This is a shorthand for calling ``get_clip_id_by_motion_name()`` and ``get_stop_time_by_clip_id()``.

        :raises MotionDataNotFoundError: if the motion data is not found in this controller
        """
        # Get the clip ID
        try:
            clip_id = self.get_clip_id_by_motion_name(motion_name)
        except KeyError as ex:
            raise MotionDataNotFoundError(motion_name, error_msg) from ex

        # Check if an :class:`AnimatorOverrideController` is provided.
        # If not provided, return the animation stop time of the clip ID obtained above
        if not override:
            return self.get_stop_time_by_clip_id(clip_id)

        # Check if the clip is overridden. If so, return the stop time of the overriding clip
        if override.is_clip_overridden(clip_id):
            return override.get_stop_time_by_original_clip_id(clip_id)

        # Clip not overridden, return the stop time of the original animation clip
        return self.get_stop_time_by_clip_id(clip_id)

    @staticmethod
    @abstractmethod
    def parse_raw(data: dict[str, Union[str, int, float]]) -> "AnimatorController":
        """Parse a raw data entry to be the asset entry class."""
        raise NotImplementedError()
