"""Classes for the animation clip data."""
from dataclasses import dataclass, field
from typing import Any

__all__ = ("AnimationClipDataAnimatorController", "AnimationClipDataAnimatorOverrideController")


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
