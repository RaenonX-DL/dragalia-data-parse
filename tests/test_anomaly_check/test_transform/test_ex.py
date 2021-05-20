import pytest

from dlparse.errors import AbilityConditionUnconvertibleError, AbilityVariantUnconvertibleError
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer
from tests.utils import UnknownAbilityData, UnknownAbilityDataCollection


@pytest.mark.holistic
def test_transform_all_character_ex(transformer_ability: AbilityTransformer, asset_manager: AssetManager):
    unknown_abilities = UnknownAbilityDataCollection()
    counter: int = 0

    # Not checking all abilities in the ability asset directly
    # because there are some unused or deprecated ability inside.
    # We don't want to spend time handling unused things.
    for chara_data in asset_manager.asset_chara_data.playable_data:
        ex_id = chara_data.ex_id_at_max_level
        counter += 1

        try:
            ex_ability_data = transformer_ability.transform_ex_ability(ex_id)

            unknown_abilities.add_data_if_needed(
                chara_data, ex_id, ex_ability_data, check_effective_for_team=True
            )
        except (AbilityConditionUnconvertibleError, AbilityVariantUnconvertibleError) as ex:
            # Condition/Variant unconvertible (most likely due to unknown/unhandled condition/variant)
            ex_ability_data = asset_manager.asset_ex_ability.get_data_by_id(ex_id)

            condition_ids = (
                {ex_id: ex_ability_data.condition.condition_code}
                if ex_ability_data.condition.is_unknown_condition else {}
            )

            unknown_abilities.add_data(UnknownAbilityData(
                chara_id=chara_data.id, ability_id=ex_id,
                condition_ids=condition_ids,
                variant_ids={ex_id: ex_ability_data.unknown_variant_type_ids},
                error=ex
            ))

    unknown_abilities.print_and_fail_if_any(counter)
