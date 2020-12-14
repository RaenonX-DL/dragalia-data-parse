from dlparse.mono.manager import AssetManager
from dlparse.transformer import AbilityTransformer


def test_transform_all_character_ability(transformer_ability: AbilityTransformer, asset_manager: AssetManager):
    for chara_data in asset_manager.asset_chara_data:
        for ability_id in chara_data.ability_ids_all_level:
            # FIXME: Check for any unknown conditions
            ability_data = transformer_ability.transform_ability(ability_id)
