from dlparse.enums import BuffParameter, Condition, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test_def_up_on_lt_30_hp(transformer_ability: AbilityTransformer):
    # Raemond (AB1 @ Max - DEF +50% for 15s when HP < 30%)
    # https://dragalialost.gamepedia.com/Karl
    ability_data = transformer_ability.transform_ability(210001704)

    expected_info = {
        AbilityEffectInfo(
            210001704, ConditionComposite(Condition.ON_HP_LT_30), BuffParameter.DEF_BUFF, 0.5,
            max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_atk_up_shapeshifted(transformer_ability: AbilityTransformer):
    # Euden (AB1 @ Max - ATK +10%/+15%/+15% for each transform)
    # https://dragalialost.gamepedia.com/The_Prince
    ability_data = transformer_ability.transform_ability(700)

    expected_info = {
        AbilityEffectInfo(
            700, ConditionComposite(Condition.SELF_SHAPESHIFTED_1_TIME),
            BuffParameter.ATK_BUFF, 0.1
        ),
        AbilityEffectInfo(
            700, ConditionComposite(Condition.SELF_SHAPESHIFTED_2_TIMES),
            BuffParameter.ATK_BUFF, 0.15
        ),
        AbilityEffectInfo(
            700, ConditionComposite(Condition.SELF_SHAPESHIFTED_3_TIMES),
            BuffParameter.ATK_BUFF, 0.15
        ),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)


def test_atk_up_on_def_buffed(transformer_ability: AbilityTransformer):
    # Valentine's Orion (AB1 @ Max - DEF doublebuff - ATK +15% (Buff))
    # https://dragalialost.gamepedia.com/Valentine%27s_Orion
    ability_data = transformer_ability.transform_ability(210000607)

    expected_info = {
        AbilityEffectInfo(210000607, ConditionComposite(Condition.ON_BUFFED_DEF), BuffParameter.ATK_BUFF, 0.15),
    }

    check_ability_effect_unit_match(ability_data.effect_units, expected_info)
