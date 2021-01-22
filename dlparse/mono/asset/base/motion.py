"""Base classes for the motion asset files."""
import json
from abc import ABC, abstractmethod
from typing import Any, Generic, TextIO, Type, TypeVar

from .asset import get_file_like, get_file_path
from .entry import EntryBase

__all__ = ("MotionControllerBase", "MotionSelectorBase", "parse_motion_data")


def parse_motion_data(file_like: TextIO) -> dict[str, Any]:
    """
    Parse ``file_like`` to a :class:`dict`.

    This method opens and closes ``file_like``.
    """
    with file_like:
        data = json.load(file_like)

    return data


class MotionControllerBase(EntryBase, ABC):
    """
    Base class of a motion controller.

    A controller selects the animation clip to be used for a certain motion.
    """

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
