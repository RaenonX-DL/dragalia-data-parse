"""Motion controller classes for a single weapon type."""
from dataclasses import dataclass, field
from typing import Any

from dlparse.enums import Weapon
from dlparse.mono.asset.base import MotionControllerBase, MotionSelectorBase
from .clip import AnimationClipDataAnimatorController

__all__ = ("MotionControllerWeapon", "MotionSelectorWeapon")


@dataclass
class MotionControllerWeapon(MotionControllerBase):
    """Motion controller for a single weapon type."""

    # Init vars
    json_dict: dict[str, Any]

    # Parsed vars
    weapon: Weapon = field(init=False)
    tos: dict[str, int] = field(init=False)  # K = motion name, V = state machine name ID
    state_machine_ref: dict[int, int] = field(init=False)  # K = state machine name ID, V = clip index (0-based)
    animation_clip_path_ids: list[int] = field(init=False)

    # --- K = animation clip ID, V = animation clip data
    animation_clips: dict[int, AnimationClipDataAnimatorController] = field(init=False)

    def __post_init__(self):
        controller = self.json_dict["$Controller"]
        clips = self.json_dict["$Clips"]

        self.weapon = Weapon.from_str(controller["m_Name"])

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

    @staticmethod
    def parse_raw(data: dict[str, Any]) -> "MotionControllerWeapon":
        return MotionControllerWeapon(data)


@dataclass
class MotionSelectorWeapon(MotionSelectorBase[Weapon, MotionControllerWeapon]):
    """Class to select the controller to be used based on the weapon type."""

    def __init__(self, motion_dir: str):
        motion_map = {weapon: f"{weapon.weapon_str}.json" for weapon in Weapon.get_all_valid_weapons()}

        super().__init__(MotionControllerWeapon, motion_dir, motion_map)
