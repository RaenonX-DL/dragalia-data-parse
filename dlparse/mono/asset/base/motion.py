"""Base implementations for handling the motion asset files."""
import json
from abc import ABC
from typing import Any, TextIO

__all__ = ("parse_motion_data", "AnimationControllerBase")


def parse_motion_data(file_like: TextIO) -> dict[str, Any]:
    """
    Parse ``file_like`` to a :class:`dict`.

    This method opens and closes ``file_like``.
    """
    with file_like:
        data = json.load(file_like)

    return data


class AnimationControllerBase(ABC):
    """
    Base class of an animation controller.

    The "animation controlles" mentioned above includes:
    - ``AnimatorController``
    - ``AnimatorOverrideController``
    """
    """Base class of an animation controller."""

    # Init vars
    json_dict: dict[str, Any]
