"""Classes for managing the story data."""
import os
from functools import cache
from typing import TYPE_CHECKING

from dlparse.enums import Language, StoryType, UnitType
from dlparse.errors import StoryUnavailableError, UnknownStoryTypeError
from dlparse.mono.asset import MasterAssetIdType, StoryData, StoryImageAsset, StoryNameAsset
from dlparse.utils import localize_asset_path

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("StoryLoader",)

_unit_type_path: dict[UnitType, str] = {
    UnitType.CHARACTER: "chara",
    UnitType.DRAGON: "dragon"
}


class StoryLoader:
    """Class to load the story data."""

    # pylint: disable=too-few-public-methods

    def __init__(self, story_dir: str, asset_manager: "AssetManager") -> None:
        self._story_dir = story_dir
        self._name_asset = StoryNameAsset(story_dir)
        self._image_asset = StoryImageAsset(story_dir)
        self._asset_manager = asset_manager

    @cache
    def _get_story_name(self, story_type: StoryType, lang: Language, story_id: MasterAssetIdType) -> str:
        if story_type == StoryType.UNIT:
            unit_story_entry = self._asset_manager.asset_story_unit.get_data_by_id(story_id)
            return self._asset_manager.asset_text_multi.get_text(lang.value, unit_story_entry.title_label)

        raise UnknownStoryTypeError(story_type)

    @cache
    def _get_story_data(
            self, path_in_dir: str, story_type: StoryType, lang: Language, story_id: MasterAssetIdType
    ) -> StoryData:
        return StoryData(
            localize_asset_path(os.path.join(self._story_dir, path_in_dir, f"{story_id}.json"), lang),
            lang,
            self._get_story_name(story_type, lang, story_id),
            self._name_asset,
            self._image_asset,
        )

    def load_unit_story(self, lang: Language, unit_type: UnitType, story_id: MasterAssetIdType) -> StoryData:
        """Load the unit story given ``unit_type`` and ``story_id`` in ``lang``."""
        unit_story_dir = _unit_type_path.get(unit_type)
        if not unit_story_dir:
            raise StoryUnavailableError(f"Unit type {unit_type} does not have story")

        return self._get_story_data(os.path.join("unitstory", unit_story_dir), StoryType.UNIT, lang, story_id)
