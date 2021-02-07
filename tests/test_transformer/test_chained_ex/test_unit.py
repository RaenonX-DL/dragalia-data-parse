from dlparse.enums import BuffParameter, Condition, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test_joker(transformer_ability: AbilityTransformer):
    # Joker - 10350505
    # https://dragalialost.wiki/w/Joker
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000863)

    expected_info = {
        AbilityEffectInfo(
            400000863, ConditionComposite([Condition.TARGET_SHADOW, Condition.ON_COMBO_GTE_10]),
            BuffParameter.RESISTANCE_LIGHT_BUFF, 0.1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_mona(transformer_ability: AbilityTransformer):
    # Mona - 10150304
    # https://dragalialost.wiki/w/Mona
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000879)

    expected_info = {
        AbilityEffectInfo(
            400000879, ConditionComposite([Condition.TARGET_WIND, Condition.ON_COMBO_GTE_10]),
            BuffParameter.RESISTANCE_WATER_BUFF, 0.1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_sophie(transformer_ability: AbilityTransformer):
    # Sophie - 10450404
    # https://dragalialost.wiki/w/Sophie
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000868)

    expected_info = {
        AbilityEffectInfo(
            400000868, ConditionComposite([Condition.TARGET_LIGHT]),
            BuffParameter.RP_UP, 0.2
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_panther(transformer_ability: AbilityTransformer):
    # Panther - 10550104
    # https://dragalialost.wiki/w/Panther
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000817)

    expected_info = {
        AbilityEffectInfo(
            400000817, ConditionComposite([Condition.TARGET_FLAME]),
            BuffParameter.DRAGON_TIME, 0.2
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)
