"""Implementations for managing the story image mapping."""
from typing import Iterator, Optional

from dlparse.errors import StoryImageNotFoundError
from dlparse.mono.asset.base import AssetBase
from .base import StoryAssetParser

__all__ = ("StoryImageAsset",)

StoryImageMapping = dict[str, str]


class StoryImageAsset(AssetBase[StoryImageMapping, tuple[str, str]]):
    """Contains the story image mapping."""

    asset_file_name = "function.json"

    def __init__(self, story_dir: str) -> None:
        super().__init__(StoryAssetParser, asset_dir=story_dir)

    def __iter__(self) -> Iterator[tuple[str, str]]:
        # False-negative
        # noinspection PyTypeChecker
        return iter(self.data.items())

    def get_image_name(self, image_code: Optional[str], on_not_found: str = "(throw)") -> Optional[str]:
        """
        Get the image name of ``image_code``.

        Returns ``None`` if ``image_code`` is falsy.

        Raises :class:`StoryImageNotFoundError` if ``image_code`` does not have a corresponding image name
        and ``on_not_found`` is "(throw)" or not specified.
        """
        if not image_code:
            return None

        ret = self.data.get(image_code)

        if not ret:
            if on_not_found == "(throw)":
                raise StoryImageNotFoundError(image_code)

            return on_not_found

        return ret
