from dlparse.enums import AbilityTargetAction, BuffParameter, Condition, ConditionComposite
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


def test_euden_ab3_max(transformer_ability: AbilityTransformer):
    # Euden (AB3 @ Max - Player EXP +15% / Normal attack dispel buffs in dragon)
    # https://dragalialost.gamepedia.com/The_Prince
    ability_data = transformer_ability.transform_ability(688)

    expected_info = {
        AbilityEffectInfo(
            688, ConditionComposite(), BuffParameter.PLAYER_EXP, 0.15, target_action=AbilityTargetAction.NONE
        ),
        AbilityEffectInfo(
            689, ConditionComposite(Condition.SELF_SHAPESHIFTED_1_TIME_IN_DRAGON), BuffParameter.DISPEL, 0,
            target_action=AbilityTargetAction.AUTO
        ),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_gala_mym_ab1_max(transformer_ability: AbilityTransformer):
    # Gala Mym (AB1 @ Max)
    # - Burn Res 100%
    # - Permanent ATK +15% for the first shapeshift
    # - Permanent S2 enhancement
    # - ASPD +15% in dragon from the second shapeshift
    # https://dragalialost.gamepedia.com/Gala_Mym
    ability_data = transformer_ability.transform_ability(238)

    expected_info = {
        AbilityEffectInfo(
            240, ConditionComposite(Condition.SELF_SHAPESHIFTED_1_TIME),
            BuffParameter.ATK_BUFF, 0.15, max_occurrences=1
        ),
        AbilityEffectInfo(
            422, ConditionComposite(Condition.SELF_SHAPESHIFTED_2_TIMES_IN_DRAGON),
            BuffParameter.ASPD_PASSIVE, 0.15, max_occurrences=0
        ),
        AbilityEffectInfo(
            423, ConditionComposite(), BuffParameter.RESISTANCE_BURN, 1.0,
            max_occurrences=0
        ),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)
