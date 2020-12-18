"""Class to transform abilities."""
from typing import TYPE_CHECKING

from dlparse.model import AbilityData

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("AbilityTransformer",)


class AbilityTransformer:
    """Class to transform the ability data."""

    # pylint: disable=too-few-public-methods

    def __init__(self, asset_manager: "AssetManager"):
        self._asset_manager: "AssetManager" = asset_manager

    def transform_ability(self, ability_id: int) -> AbilityData:
        """Transform ``ability_id`` to an ability data."""
        ability_data = self._asset_manager.asset_ability_data.get_data_by_id(ability_id)

        return AbilityData(
            self._asset_manager,
            ability_data.get_all_ability(self._asset_manager.asset_ability_data)
        )
