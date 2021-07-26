"""Util functions for processing ability data."""
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from dlparse.mono.asset import AbilityAsset, AbilityEntry

__all__ = ("get_ability_data_to_shift_hit_attr",)


def get_ability_data_to_shift_hit_attr(
        ability_ids: list[int], ability_asset: "AbilityAsset"
) -> Optional["AbilityEntry"]:
    """Get the ability in ``ability_ids`` that shifts hit attribute if any."""
    ability_data_all = [
        ability_data
        for ability_id in ability_ids
        for ability_data in ability_asset.get_data_by_id(ability_id).get_all_ability(ability_asset).values()
    ]
    ability_data_hit_attr_shift = next(
        (
            ability_data
            for ability_data in ability_data_all
            for variant in ability_data.variants
            if variant.is_hit_attr_shift
        ),
        None
    )

    return ability_data_hit_attr_shift
