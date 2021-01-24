from dataclasses import dataclass
from typing import Optional

import pytest

from dlparse.enums import HitTargetSimple
from dlparse.errors import AbilityConditionUnconvertibleError, AbilityVariantUnconvertibleError
from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer


@dataclass
class UnknownAbilityData:
    chara_id: int
    cex_ability_id: int

    condition_ids: dict[int, int]
    variant_ids: dict[int, list[int]]

    error: Optional[Exception] = None

    def __str__(self):
        return repr(self)

    def __repr__(self):
        ret = f"- #{self.cex_ability_id} ({self.chara_id})"

        for source_ab_id, condition_id in self.condition_ids.items():
            ret += f"\n  - Condition ID: {condition_id} from #{source_ab_id}"

        for source_ab_id, variant_type_ids in self.variant_ids.items():
            ret += f"\n  - Variant type IDs: {variant_type_ids} from #{source_ab_id}"

        if self.error:
            ret += f"\n  - Error: {self.error}"

        return ret


def test_transform_all_character_chained_ex(transformer_ability: AbilityTransformer, asset_manager: AssetManager):
    unknown_abilities: list[UnknownAbilityData] = []
    counter: int = 0

    # Not checking all abilities in the ability asset directly
    # because there are some unused or deprecated ability inside.
    # We don't want to spend time handling unused things.
    for chara_data in asset_manager.asset_chara_data.playable_chara_data:
        cex_id = chara_data.cex_id_at_max_level
        counter += 1

        try:
            chained_ex_ability_data = transformer_ability.transform_chained_ex_ability(cex_id)

            # Check if any unknown elements exist but no error yielded
            if chained_ex_ability_data.has_unknown_elements:
                unknown_abilities.append(UnknownAbilityData(
                    chara_id=chara_data.id, cex_ability_id=cex_id,
                    condition_ids=chained_ex_ability_data.unknown_condition_ids,
                    variant_ids=chained_ex_ability_data.unknown_variant_ids
                ))

            # Ability should be effective to the whole team
            if any(unit.target != HitTargetSimple.TEAM for unit in chained_ex_ability_data.effect_units):
                pytest.fail(
                    f"Ability target not effective to the whole team where it should: #{cex_id})"
                )
        except (AbilityConditionUnconvertibleError, AbilityVariantUnconvertibleError) as ex:
            # Condition/Variant unconvertible (most likely due to unknown/unhandled condition/variant)
            chained_ex_ability_data = asset_manager.asset_ability_data.get_data_by_id(cex_id)

            condition_ids = (
                {cex_id: chained_ex_ability_data.condition.condition_code}
                if chained_ex_ability_data.condition.is_unknown_condition else {}
            )

            unknown_abilities.append(UnknownAbilityData(
                chara_id=chara_data.id, cex_ability_id=cex_id,
                condition_ids=condition_ids,
                variant_ids={cex_id: chained_ex_ability_data.unknown_variant_type_ids},
                error=ex
            ))

    if unknown_abilities:
        unknown_str = "\n".join([str(entry) for entry in unknown_abilities])
        pytest.fail(
            f"{len(unknown_abilities)} abilities have unknown elements "
            f"(total {counter}, {1 - len(unknown_abilities) / counter:.2%} parsed):\n"
            f"{unknown_str}"
        )
