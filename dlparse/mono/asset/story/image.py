"""Implementations for managing the story image mapping."""
import glob
import os
from typing import Iterator, Optional

from dlparse.errors import StoryImageUnavailableError
from dlparse.mono.asset.base import AssetBase
from dlparse.utils import make_path
from .base import StoryAssetParser

__all__ = ("StoryImageAsset",)

StoryImageMapping = dict[str, str]

_ID_PREFIX: dict[str, str] = {
    "m": "100",
    "n": "120",
    "p": "110",
    "b": "210",
}

_PREFIX_SKIP: list[str] = [
    "raid",  # Raid event CG
    "common",  # Common CG
    "mainstory",  # Mainstory CG
    "facility",  # Facility event CG
]


def _translate_image_code(image_code: str) -> Optional[str]:
    """
    Translate ``image_code`` to image name according to some rules.

    Returns ``None`` if the prefix of the image code is unhandled.
    """
    prefix = image_code[0]

    if prefix not in _ID_PREFIX:
        return None

    image_code = image_code.replace(prefix, _ID_PREFIX[prefix])
    return f"{image_code[:6]}_{image_code[6:]}"


class StoryImageAsset(AssetBase[StoryImageMapping, tuple[str, str]]):
    """Contains the story image mapping."""

    asset_file_name = "function.json"

    def _init_image_dir_dict(self, image_dir: str):
        self._image_dir_dict = {}
        for file_path in glob.glob(f"{image_dir}/**/*.png", recursive=True):
            image_rel_path = os.path.relpath(file_path, image_dir)
            image_name = os.path.splitext(os.path.basename(image_rel_path))[0]

            self._image_dir_dict[image_name] = make_path(image_rel_path, is_net=True)

    def __init__(self, story_dir: str, image_dir: str, /, is_image_dir_net: bool = False) -> None:
        super().__init__(StoryAssetParser, asset_dir=story_dir)

        self._image_dir_dict: Optional[dict[str, str]] = None
        # Initialize the image path mapping only if the image directory is not a network path
        if not is_image_dir_net:
            self._init_image_dir_dict(image_dir)

    def __iter__(self) -> Iterator[tuple[str, str]]:
        # False-negative
        # noinspection PyTypeChecker
        return iter(self.data.items())

    def get_image_name(self, image_code: Optional[str]) -> Optional[str]:
        """
        Get the image name of ``image_code``.

        Returns ``None`` if ``image_code`` is falsy or the code prefix is to be skipped.

        Raises :class:`StoryImageUnavailableError` if ``image_code`` does not have a corresponding image name.
        """
        if not image_code:
            return None

        # Has to place before `_translate_image_code`
        # because the prefix used for translation could have prefix conflict (for example, `m` and `mainstory`)
        if any(image_code.startswith(prefix) for prefix in _PREFIX_SKIP):
            return None

        if ret := self.data.get(image_code):
            # Data may contain some variant like `100009_06_01`, this should be mapped as `100009_06`
            # Therefore, trimming the return
            return ret[:9]

        if ret := _translate_image_code(image_code):
            return ret

        # For some reason, image code could be found already translated in the story data
        # One IRL case is `110267_02` (Hawk)
        if image_code in self.data.values():
            return image_code

        raise StoryImageUnavailableError(image_code)

    def get_image_path(self, image_code: Optional[str]) -> Optional[str]:
        """
        Get the network image path rooted from ``image_dir`` when initialized of ``image_code``.

        Returns ``None`` if ``image_code`` is falsy or the code prefix is to be skipped.

        Raises :class:`StoryImageUnavailableError` if ``image_code`` does not have a corresponding image name.

        **This can't be used when the image directory is a network source.**
        Doing so raises :class:`StoryImageUnavailableError`.
        """
        # Explicit check because it could be an empty dict if the image directory contains nothing
        if self._image_dir_dict is None:
            raise StoryImageUnavailableError(
                "Image path unavailable because the image directory is a network source."
            )

        image_name = self.get_image_name(image_code)
        if not image_name:
            return None

        if image_path := self._image_dir_dict.get(image_name):
            return image_path

        raise StoryImageUnavailableError(image_code)
