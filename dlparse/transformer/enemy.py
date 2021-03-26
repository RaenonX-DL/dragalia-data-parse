"""Enemy data transformer."""
from typing import TYPE_CHECKING

from dlparse.model import EnemyData

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("EnemyTransformer",)


class EnemyTransformer:
    """Class to transform an enemy data."""

    # pylint: disable=too-few-public-methods

    def __init__(self, asset_manager: "AssetManager"):
        self._asset_manager: "AssetManager" = asset_manager

    def transform_enemy_data(self, enemy_param_id: int) -> EnemyData:
        """Transform ``enemy_param_id`` to an enemy info."""
        enemy_param_data = self._asset_manager.asset_enemy_param.get_data_by_id(enemy_param_id)

        return EnemyData(self._asset_manager, enemy_param_data)
