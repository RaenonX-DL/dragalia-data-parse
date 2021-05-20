import pytest

from dlparse.errors import AbilityConditionUnconvertibleError, AbilityVariantUnconvertibleError
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer
from tests.utils import UnknownAbilityData, UnknownAbilityDataCollection


@pytest.mark.skip
def test_transform_all_character_ability(transformer_ability: AbilityTransformer, asset_manager: AssetManager):
    unknown_abilities = UnknownAbilityDataCollection()
    counter: int = 0

    # Not checking all abilities in the ability asset directly
    # because there are some unused or deprecated ability inside.
    # We don't want to spend time handling unused things.
    for chara_data in asset_manager.asset_chara_data.playable_data:
        for ability_id in chara_data.ability_ids_all_level:
            counter += 1

            try:
                ability_data = transformer_ability.transform_ability(ability_id)

                unknown_abilities.add_data_if_needed(chara_data, ability_id, ability_data)
            except (AbilityConditionUnconvertibleError, AbilityVariantUnconvertibleError) as ex:
                # Condition/Variant unconvertible (most likely due to unknown/unhandled condition/variant)
                ability_data = asset_manager.asset_ability_data.get_data_by_id(ability_id)

                unknown_abilities.add_data(UnknownAbilityData(
                    chara_data.id, ability_id,
                    ({ability_id: ability_data.condition.condition_code}
                     if ability_data.condition.is_unknown_condition else {}),
                    {ability_id: ability_data.unknown_variant_type_ids},
                    ex
                ))

    unknown_abilities.print_and_fail_if_any(counter)
