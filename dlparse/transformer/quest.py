"""Quest data transformer."""
from typing import TYPE_CHECKING

from dlparse.model import QuestData

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("QuestTransformer",)


class QuestTransformer:
    """Class to transform a quest data."""

    # pylint: disable=too-few-public-methods

    def __init__(self, asset_manager: "AssetManager"):
        self._asset_manager: "AssetManager" = asset_manager

    def transform_quest_data(self, quest_id: int) -> QuestData:
        """Transform ``enemy_param_id`` to an enemy info."""
        quest_data = self._asset_manager.asset_quest_data.get_data_by_id(quest_id)

        return QuestData(self._asset_manager, quest_data)
