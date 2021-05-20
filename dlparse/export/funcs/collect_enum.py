"""Functions to collect the enums to be exported."""
from typing import Callable, TypeVar

from dlparse.enums import BuffParameter
from dlparse.model import AbilityDataBase
from dlparse.mono.asset import CharaDataEntry
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer

__all__ = ("collect_ex_ability_buff_param", "collect_chained_ex_ability_buff_param")

T = TypeVar("T", bound=AbilityDataBase)


def collect_ability_data_buff_param(
        asset_manager: AssetManager, transform_fn: Callable[[CharaDataEntry], T]
) -> list[BuffParameter]:
    """Collect buff parameters from the transformed ability data for each character and compose an image path map."""
    units: set[BuffParameter] = set()

    for chara_data in asset_manager.asset_chara_data.playable_data:
        units.update(effect_unit.parameter for effect_unit in transform_fn(chara_data).effect_units)

    # Sort the buff paramters by its value to ensure the order will not change frequently,
    # avoiding unnecessary export data updates
    return list(sorted(units, key=lambda item: item.value))


def collect_ex_ability_buff_param(
        transformer_ability: AbilityTransformer, asset_manager: AssetManager
) -> list[BuffParameter]:
    """Collect all possible buff parameters from all EX abilities and compose an image path map."""
    return collect_ability_data_buff_param(
        asset_manager,
        lambda chara_data: transformer_ability.transform_ex_ability(chara_data.ex_id_at_max_level)
    )


def collect_chained_ex_ability_buff_param(
        transformer_ability: AbilityTransformer, asset_manager: AssetManager
) -> list[BuffParameter]:
    """Collect all possible buff parameters from all chained EX abilities and compose an image path map."""
    return collect_ability_data_buff_param(
        asset_manager,
        lambda chara_data: transformer_ability.transform_chained_ex_ability(chara_data.cex_id_at_max_level)
    )
