from dlparse.enums import BuffParameter, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test_joker(transformer_ability: AbilityTransformer):
    # Joker - 10350505
    # https://dragalialost.wiki/w/Joker
    ex_ability_data = transformer_ability.transform_ex_ability(101100007)

    expected_info = {
        AbilityEffectInfo(
            101100007, ConditionComposite(),
            BuffParameter.ASPD_PASSIVE, 0.07
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_mona(transformer_ability: AbilityTransformer):
    # Mona - 10150304
    # https://dragalialost.wiki/w/Mona
    ex_ability_data = transformer_ability.transform_ex_ability(157570005)

    expected_info = {
        AbilityEffectInfo(
            157570005, ConditionComposite(),
            BuffParameter.WIND_ELEM_DMG_UP, 0.2, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_sophie(transformer_ability: AbilityTransformer):
    # Sophie - 10450404
    # https://dragalialost.wiki/w/Sophie
    ex_ability_data = transformer_ability.transform_ex_ability(157570413)

    expected_info = {
        AbilityEffectInfo(
            157570413, ConditionComposite(),
            BuffParameter.LIGHT_ELEM_DMG_UP, 0.15
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_panther(transformer_ability: AbilityTransformer):
    # Panther - 10550104
    # https://dragalialost.wiki/w/Panther
    ex_ability_data = transformer_ability.transform_ex_ability(103150005)

    expected_info = {
        AbilityEffectInfo(
            103150005, ConditionComposite(),
            BuffParameter.INFLICT_PROB_SCORCHREND, 0.2
        ),
        AbilityEffectInfo(
            103150005, ConditionComposite(),
            BuffParameter.DURATION_EXT_SCORCHREND, 0.2
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)
