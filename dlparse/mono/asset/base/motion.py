"""Base classes for the motion asset files."""
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, TextIO, Type, TypeVar

from .asset import get_file_like, get_file_path
from .entry import EntryBase

__all__ = (
    "parse_motion_data", "MotionControllerBase", "MotionSelectorBase",
    "AnimationClipDataAnimatorController", "AnimationClipDataAnimatorOverrideController"
)


def parse_motion_data(file_like: TextIO) -> dict[str, Any]:
    """
    Parse ``file_like`` to a :class:`dict`.

    This method opens and closes ``file_like``.
    """
    with file_like:
        data = json.load(file_like)

    return data


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


class MotionControllerBase(EntryBase, ABC):
    """
    Base class of a motion controller.

    A controller selects the animation clip to be used for a certain motion.
    """

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
    @abstractmethod
    def parse_raw(data: dict[str, Any]) -> "MotionControllerBase":
        """Parse a raw data entry to a motion controller."""
        raise NotImplementedError()


KT = TypeVar("KT")
CT = TypeVar("CT", bound=MotionControllerBase)


class MotionSelectorBase(Generic[KT, CT], ABC):
    """
    Base class of a motion selector.

    A selector selects a the controller to be used.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, controller_cls: Type[CT], motion_dir: str, motion_map: dict[KT, str]):
        """
        Initializes a motion selector.

        The key of ``motion_map`` will be used for selecting the motion controller;
        the value of ``motion_map`` is the file path of the motion controller excluding ``motion_dir``.
        """
        self._motion_controller: dict[KT, CT] = {}

        for motion_key, motion_file_path in motion_map.items():
            file_path = get_file_path(motion_file_path, asset_dir=motion_dir)
            file_like = get_file_like(file_path)

            self._motion_controller[motion_key] = controller_cls.parse_raw(parse_motion_data(file_like))

    def get_controller(self, key: KT) -> CT:
        """Get the controller mapped to ``key``. Returns ``None`` if not found."""
        return self._motion_controller.get(key)
