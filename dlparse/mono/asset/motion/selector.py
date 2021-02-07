"""Base classes for a motion selector."""
from abc import ABC
from typing import Generic, Type, TypeVar

from dlparse.mono.asset.base import get_file_like, get_file_path, parse_motion_data
from dlparse.mono.asset.extension import AnimatorController

KT = TypeVar("KT")
CT = TypeVar("CT", bound=AnimatorController)


class MotionSelectorBase(Generic[KT, CT], ABC):
    """
    Base class of a motion selector.

    A selector selects a the controller to be used.

    A difference between ``MotionSelector`` and ``MotionLoader`` is that
    ``MotionSelector`` preloads all controllers during initialization, while
    ``MotionLoader`` loads the controllers on-demand.
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
