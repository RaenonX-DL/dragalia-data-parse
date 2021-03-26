"""Classes for handling the dungeon planner asset."""
from dataclasses import dataclass
from typing import Optional, TextIO, Union

from dlparse.mono.asset.base import MasterAssetBase, MasterEntryBase, MasterParserBase

__all__ = ("DungeonPlannerEntry", "DungeonPlannerAsset")

DUNGEON_VARIATION_COUNT_MAX: int = 10


@dataclass
class DungeonPlannerEntry(MasterEntryBase):
    """Single entry of a dungeon planner data."""

    bgm_id: str

    enemy_param_ids: list[list[int]]  # Index = ``variation_idx`` of the quest data

    @staticmethod
    def get_enemy_param_ids(data: dict[str, Union[str, int]]) -> list[list[int]]:
        """
        Get the enemy parameter IDs.

        The index of the return corresponds to ``variation_idx`` field of the quest data.

        This filters unused fields.
        """
        param_ids = []
        param_fields = [
            [
                "_BossCameraEnemy0Param",
                "_BossCameraEnemy1Param",
                "_BossCameraEnemy2Param",
                "_BossCameraEnemy3Param",
                "_BossCameraEnemy4Param",
                "_BossCameraEnemy5Param",
                "_BossCameraEnemy6Param",
                "_BossCameraEnemy7Param",
                "_BossCameraEnemy8Param",
                "_BossCameraEnemy9Param"
            ],
            ["_BossCameraEnemy0ParamHard"],
            ["_BossCameraEnemy0ParamVeryhard"],
            ["_BossCameraEnemy0ParamExtreme"],
            ["_BossCameraEnemy0ParamHell"],
            ["_BossCameraEnemy0Param6"],
            ["_BossCameraEnemy0Param7"],
            ["_BossCameraEnemy0Param8"],
            ["_BossCameraEnemy0Param9"],
            ["_BossCameraEnemy0Param10"],
        ]

        for variation_fields in param_fields:
            param_ids_variation = []

            for variation_field in variation_fields:
                # REMOVE: not with walrus https://github.com/PyCQA/pylint/issues/3249
                # pylint: disable=superfluous-parens
                if not (enemy_param_id := data[variation_field]):
                    continue

                param_ids_variation.append(enemy_param_id)

            param_ids.append(param_ids_variation)

        return param_ids

    @staticmethod
    def parse_raw(data: dict[str, Union[str, int]]) -> "DungeonPlannerEntry":
        return DungeonPlannerEntry(
            id=data["_Area"],
            bgm_id=data["_Bgm"],
            enemy_param_ids=DungeonPlannerEntry.get_enemy_param_ids(data),
        )


class DungeonPlannerAsset(MasterAssetBase[DungeonPlannerEntry]):
    """Quest data asset class."""

    asset_file_name = "DungeonAreaPlannerData.json"

    def __init__(
            self, file_location: Optional[str] = None, /,
            asset_dir: Optional[str] = None, file_like: Optional[TextIO] = None
    ):
        super().__init__(DungeonPlannerParser, file_location, asset_dir=asset_dir, file_like=file_like)


class DungeonPlannerParser(MasterParserBase[DungeonPlannerEntry]):
    """Class to parse the quest data file."""

    @classmethod
    def parse_file(cls, file_like: TextIO) -> dict[str, DungeonPlannerEntry]:
        entries = cls.get_entries_dict(file_like, key="_Area")

        return {key: DungeonPlannerEntry.parse_raw(value) for key, value in entries.items()}
