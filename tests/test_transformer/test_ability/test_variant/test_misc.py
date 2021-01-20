from dlparse.enums import BuffParameter, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test_dummy(transformer_ability: AbilityTransformer):
    # Gala Leonidas (AB1 @ Lv1 - Nothing)
    # https://dragalialost.gamepedia.com/Gala_Leonidas
    ability_data = transformer_ability.transform_ability(1460)

    expected_info = set()

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_player_exp(transformer_ability: AbilityTransformer):
    # Euden (AB3 @ Lv2 - Player EXP +15%)
    # https://dragalialost.gamepedia.com/The_Prince
    ability_data = transformer_ability.transform_ability(110150003)

    expected_info = {
        AbilityEffectInfo(110150003, ConditionComposite(), BuffParameter.PLAYER_EXP, 0.15),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)
