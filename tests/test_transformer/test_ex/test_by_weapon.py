from dlparse.enums import BuffParameter, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test_sword(transformer_ability: AbilityTransformer):
    # Wedding Elisanne - 10150302
    # https://dragalialost.gamepedia.com/Wedding_Elisanne
    ex_ability_data = transformer_ability.transform_ex_ability(101050010)

    expected_info = {
        AbilityEffectInfo(
            101050010, ConditionComposite(),
            BuffParameter.DP_RATE, 0.15, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_katana(transformer_ability: AbilityTransformer):
    # Nobunaga - 10250103
    # https://dragalialost.gamepedia.com/Nobunaga
    ex_ability_data = transformer_ability.transform_ex_ability(101020010)

    expected_info = {
        AbilityEffectInfo(
            101020010, ConditionComposite(),
            BuffParameter.ATK_EX, 0.1, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_dagger(transformer_ability: AbilityTransformer):
    # Renee - 10340203
    # https://dragalialost.gamepedia.com/Renee
    ex_ability_data = transformer_ability.transform_ex_ability(103000010)

    expected_info = {
        AbilityEffectInfo(
            103000010, ConditionComposite(),
            BuffParameter.CRT_RATE, 0.1, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_axe(transformer_ability: AbilityTransformer):
    # Ramona - 10450101
    # https://dragalialost.gamepedia.com/Ramona
    ex_ability_data = transformer_ability.transform_ex_ability(101030010)

    expected_info = {
        AbilityEffectInfo(
            101030010, ConditionComposite(),
            BuffParameter.DEF_PASSIVE, 0.15, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_lance(transformer_ability: AbilityTransformer):
    # Gala Mym - 10550101
    # https://dragalialost.gamepedia.com/Gala_Mym
    ex_ability_data = transformer_ability.transform_ex_ability(101010010)

    expected_info = {
        AbilityEffectInfo(
            101010010, ConditionComposite(),
            BuffParameter.HP_RAISE_BY_MAX, 0.15, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_bow(transformer_ability: AbilityTransformer):
    # Meene - 10650303
    # https://dragalialost.gamepedia.com/Meene
    ex_ability_data = transformer_ability.transform_ex_ability(101040010)

    expected_info = {
        AbilityEffectInfo(
            101040010, ConditionComposite(),
            BuffParameter.SP_RATE, 0.15, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_wand(transformer_ability: AbilityTransformer):
    # Veronica - 10750501
    # https://dragalialost.gamepedia.com/Veronica
    ex_ability_data = transformer_ability.transform_ex_ability(102000010)

    expected_info = {
        AbilityEffectInfo(
            102000010, ConditionComposite(),
            BuffParameter.SKILL_DAMAGE, 0.15, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_staff(transformer_ability: AbilityTransformer):
    # Aurien - 10830101
    # https://dragalialost.gamepedia.com/Aurien
    ex_ability_data = transformer_ability.transform_ex_ability(104000010)

    expected_info = {
        AbilityEffectInfo(
            104000010, ConditionComposite(),
            BuffParameter.HEAL_RP, 0.2, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_gun(transformer_ability: AbilityTransformer):
    # Ilia - 10950401
    # https://dragalialost.gamepedia.com/Ilia
    ex_ability_data = transformer_ability.transform_ex_ability(109000009)

    expected_info = {
        AbilityEffectInfo(
            109000009, ConditionComposite(),
            BuffParameter.OD_GAUGE_DAMAGE, 0.2, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)
