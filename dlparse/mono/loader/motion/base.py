"""Base class of a motion loader."""
from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

from dlparse.errors import MotionDataNotFoundError
from dlparse.mono.asset.base import AnimationControllerBase

__all__ = ("MotionLoaderBase",)

CT = TypeVar("CT", bound=AnimationControllerBase)
ET = TypeVar("ET")


class MotionLoaderBase(Generic[CT, ET], ABC):
    """
    Base class of a motion loader.

    A difference between ``MotionSelector`` and ``MotionLoader`` is that
    ``MotionSelector`` preloads all controllers during initialization, while
    ``MotionLoader`` loads the controllers on-demand.
    """

    def __init__(self, motion_root_dir: str):
        self._motion_root: str = motion_root_dir
        self._motion_cache: dict[str, CT] = {}  # K = name, V = controller

    def _get_motion_ctrl(self, entry: ET, fn_load_ctrl: Callable[[str, str], CT]) -> CT:
        """
        Get the motion controller that corresponds to ``entry``.

        ``fn_load_ctrl`` is the function to load the controller.
        The 1st argument is the root directory of the motion controller file.
        The 2nd argument is the file name of the controller, formatted as ``<CONTROLLER_NAME>.json``.

        ``<CONTROLLER_NAME>`` is obtained by calling ``get_controller_name()``.

        :raises MotionDataNotFoundError: if the motion data of ``entry`` is not found
        """
        name = self.get_controller_name(entry)

        if name not in self._motion_cache:
            try:
                self._motion_cache[name] = fn_load_ctrl(self._motion_root, f"{name}.json")
            except FileNotFoundError as ex:
                raise MotionDataNotFoundError(name) from ex

        return self._motion_cache[name]

    @abstractmethod
    def get_motion_stop_time(self, entry: ET, motion_name: str) -> float:
        """Get the motion ``motion_name`` stop time of ``entry``."""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_controller_name(entry: ET) -> str:
        """Get the controller name of ``entry``."""
        raise NotImplementedError()
