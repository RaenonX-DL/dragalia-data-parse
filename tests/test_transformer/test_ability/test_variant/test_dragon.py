from dlparse.enums import BuffParameter, Condition, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test_gala_leonidas_ab1_lv2(transformer_ability: AbilityTransformer):
    # Gala Leonidas (AB1 @ Lv2 - Shapeshifting time -50%, DP consumption -50%)
    # https://dragalialost.gamepedia.com/Gala_Leonidas
    ability_data = transformer_ability.transform_ability(1461)

    condition = ConditionComposite(Condition.SELF_GLEONIDAS_FULL_STACKS)

    expected_info = {
        AbilityEffectInfo(1461, condition, BuffParameter.DP_CONSUMPTION, -0.5),
        AbilityEffectInfo(1461, condition, BuffParameter.DRAGON_TIME_FINAL, -0.5),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)
