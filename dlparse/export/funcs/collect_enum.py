"""Functions to collect the enums to be exported."""
from dlparse.enums import BuffParameter

from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer

__all__ = ("collect_ex_ability_buff_param", "collect_chained_ex_ability_buff_param")


def collect_ex_ability_buff_param(
        transformer_ability: AbilityTransformer, asset_manager: AssetManager
) -> list[BuffParameter]:
    """Collect all possible buff parameters from all EX abilities."""
    ret: set[BuffParameter] = set()

    for chara_data in asset_manager.asset_chara_data.playable_chara_data:
        ret.update(
            effect_unit.parameter for effect_unit
            in transformer_ability.transform_ex_ability(chara_data.ex_id_at_max_level).effect_units
        )

    # Sort the buff paramters by its value to ensure the order will not change frequently,
    # avoiding unnecessary export data updates
    return list(sorted(ret, key=lambda item: item.value))


def collect_chained_ex_ability_buff_param(
        transformer_ability: AbilityTransformer, asset_manager: AssetManager
) -> list[BuffParameter]:
    """Collect all possible buff parameters from all EX abilities."""
    ret: set[BuffParameter] = set()

    for chara_data in asset_manager.asset_chara_data.playable_chara_data:
        ret.update(
            effect_unit.parameter for effect_unit
            in transformer_ability.transform_chained_ex_ability(chara_data.cex_id_at_max_level).effect_units
        )

    # Sort the buff paramters by its value to ensure the order will not change frequently,
    # avoiding unnecessary export data updates
    return list(sorted(ret, key=lambda item: item.value))
