"""Classes for managing the story data."""
import os
from functools import cache

from dlparse.enums import Language, UnitType
from dlparse.errors import StoryUnavailableError
from dlparse.mono.asset.story import StoryData, StoryNameAsset
from dlparse.utils import localize_asset_path

__all__ = ("StoryLoader",)

_unit_type_path: dict[UnitType, str] = {
    UnitType.CHARACTER: "chara",
    UnitType.DRAGON: "dragon"
}


class StoryLoader:
    """Class to load the story data."""

    # pylint: disable=too-few-public-methods

    def __init__(self, story_dir: str) -> None:
        self._story_dir = story_dir
        self._name_asset = StoryNameAsset(story_dir)

    @cache
    def _get_story_data(self, path_in_dir: str, lang: Language, story_id: int) -> StoryData:
        return StoryData(
            localize_asset_path(os.path.join(self._story_dir, path_in_dir, f"{story_id}.json"), lang),
            lang,
            self._name_asset,
        )

    def load_unit_story(self, lang: Language, unit_type: UnitType, story_id: int) -> StoryData:
        """Load the unit story given ``unit_type`` and ``story_id`` in ``lang``."""
        unit_story_dir = _unit_type_path.get(unit_type)
        if not unit_story_dir:
            raise StoryUnavailableError(f"Unit type {unit_type} does not have story")

        return self._get_story_data(os.path.join("unitstory", unit_story_dir), lang, story_id)
