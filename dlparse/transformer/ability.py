"""Class to transform abilities."""
from typing import TYPE_CHECKING

from dlparse.model import AbilityData, ChainedExAbilityData, ExAbilityData

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("AbilityTransformer",)


class AbilityTransformer:
    """Class to transform the ability data."""

    def __init__(self, asset_manager: "AssetManager"):
        self._asset_manager: "AssetManager" = asset_manager

    def transform_ability(self, ability_id: int) -> AbilityData:
        """Transform ``ability_id`` to an ability data."""
        ability_data = self._asset_manager.asset_ability_data.get_data_by_id(ability_id)

        return AbilityData(
            self._asset_manager,
            ability_data.get_all_ability(self._asset_manager.asset_ability_data)
        )

    def transform_ex_ability(self, ex_ability_id: int) -> ExAbilityData:
        """Transform ``ex_ability_id`` to an EX ability data."""
        ex_ability_data = self._asset_manager.asset_ex_ability.get_data_by_id(ex_ability_id)

        return ExAbilityData(self._asset_manager, ex_ability_data)

    def transform_chained_ex_ability(self, cex_ability_id: int) -> ChainedExAbilityData:
        """Transform ``cex_ability_id`` to a chained EX ability data."""
        ability_data = self._asset_manager.asset_ability_data.get_data_by_id(cex_ability_id)

        return ChainedExAbilityData(
            self._asset_manager,
            ability_data.get_all_ability(self._asset_manager.asset_ability_data)
        )
