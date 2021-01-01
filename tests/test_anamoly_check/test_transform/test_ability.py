from dataclasses import dataclass

import pytest

from dlparse.errors import AbilityConditionUnconvertibleError, AbilityVariantUnconvertibleError
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer


@dataclass
class UnknownAbilityData:
    chara_id: int
    ability_id: int

    condition_ids: dict[int, int]
    variant_ids: dict[int, list[int]]

    def __str__(self):
        return repr(self)

    def __repr__(self):
        ret = f"- #{self.ability_id} ({self.chara_id})"

        for source_ab_id, condition_id in self.condition_ids.items():
            ret += f"\n  - Condition ID: {condition_id} from #{source_ab_id}"

        for source_ab_id, variant_type_ids in self.variant_ids.items():
            ret += f"\n  - Variant type IDs: {variant_type_ids} from #{source_ab_id}"

        return ret


@pytest.mark.skip
def test_transform_all_character_ability(transformer_ability: AbilityTransformer, asset_manager: AssetManager):
    unknown_abilities: list[UnknownAbilityData] = []

    # Not checking all abilities in the ability asset directly
    # because there are some unused or deprecated ability inside.
    # We don't want to spend time handling unused things.
    for chara_data in asset_manager.asset_chara_data:
        for ability_id in chara_data.ability_ids_all_level:
            try:
                ability_data = transformer_ability.transform_ability(ability_id)

                # Check if any unknown elements exist but no error yielded
                if ability_data.has_unknown_elements:
                    unknown_abilities.append(UnknownAbilityData(
                        chara_data.id, ability_id,
                        ability_data.unknown_condition_ids,
                        ability_data.unknown_variant_ids
                    ))
            except (AbilityConditionUnconvertibleError, AbilityVariantUnconvertibleError):
                # Condition/Variant unconvertible (most likely due to unknown/unhandled condition/variant)
                ability_data = asset_manager.asset_ability_data.get_data_by_id(ability_id)

                unknown_abilities.append(UnknownAbilityData(
                    chara_data.id, ability_id,
                    ({ability_id: ability_data.condition.condition_code}
                     if ability_data.condition.is_unknown_condition else {}),
                    {ability_id: ability_data.unknown_variant_type_ids}
                ))

    if unknown_abilities:
        unknown_str = "\n".join([str(entry) for entry in unknown_abilities])
        pytest.fail(f"Some abilities have unknown elements:\n{unknown_str}")