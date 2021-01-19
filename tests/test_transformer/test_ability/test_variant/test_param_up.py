from dlparse.enums import BuffParameter, Condition, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test_dummy(transformer_ability: AbilityTransformer):
    # Gala Leonidas (AB1 @ Lv1 - Nothing)
    # https://dragalialost.gamepedia.com/Gala_Leonidas
    ability_data = transformer_ability.transform_ability(1460)

    expected_info = set()

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_dragon_control(transformer_ability: AbilityTransformer):
    # Gala Leonidas (AB1 @ Lv2 - Shapeshifting time -50%, DP consumption -50%)
    # https://dragalialost.gamepedia.com/Gala_Leonidas
    ability_data = transformer_ability.transform_ability(1461)

    condition = ConditionComposite(Condition.SELF_GLEONIDAS_FULL_STACKS)

    expected_info = {
        AbilityEffectInfo(1461, condition, BuffParameter.DP_CONSUMPTION, -0.5),
        AbilityEffectInfo(1461, condition, BuffParameter.DRAGON_TIME_FINAL, -0.5),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_sp_rate_up(transformer_ability: AbilityTransformer):
    # Marty (AB1 @ Max - SP Rate +10%)
    # https://dragalialost.gamepedia.com/Marty
    ability_data = transformer_ability.transform_ability(938)

    expected_info = {
        AbilityEffectInfo(938, ConditionComposite(), BuffParameter.SP_RATE, 0.1),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_resistance_up_1(transformer_ability: AbilityTransformer):
    # Marty (AB3 @ Max - Stun Res +50%)
    # https://dragalialost.gamepedia.com/Marty
    ability_data = transformer_ability.transform_ability(110020604)

    expected_info = {
        AbilityEffectInfo(110020604, ConditionComposite(), BuffParameter.RESISTANCE_STUN, 0.5),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_resistance_up_2(transformer_ability: AbilityTransformer):
    # Wedding Elisanne (AB2 @ Max - Bog Res +100%)
    # https://dragalialost.gamepedia.com/Wedding_Elisanne
    ability_data = transformer_ability.transform_ability(110020906)

    expected_info = {
        AbilityEffectInfo(110020906, ConditionComposite(), BuffParameter.RESISTANCE_BOG, 1.0),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_on_def_buffed(transformer_ability: AbilityTransformer):
    # Valentine's Orion (AB1 @ Max - DEF doublebuff - ATK +15% (Buff))
    # https://dragalialost.gamepedia.com/Valentine%27s_Orion
    ability_data = transformer_ability.transform_ability(210000607)

    expected_info = {
        AbilityEffectInfo(210000607, ConditionComposite(Condition.ON_DEF_BUFFED), BuffParameter.ATK_BUFF, 0.15),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)
