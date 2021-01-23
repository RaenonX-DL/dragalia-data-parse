from dlparse.enums import BuffParameter, Condition, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test_inflicted_target(transformer_ability: AbilityTransformer):
    # Valentine's Orion - 10130103
    # https://dragalialost.gamepedia.com/Valentine%27s_Orion
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000037)

    expected_info = {
        AbilityEffectInfo(
            400000037, ConditionComposite([Condition.TARGET_FLAME, Condition.ON_INFLICTED_BURN]),
            BuffParameter.ATK_BUFF, 0.08, duration_sec=15, cooldown_sec=10
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_hp_threshold(transformer_ability: AbilityTransformer):
    # Original Karina - 10440201
    # https://dragalialost.gamepedia.com/Karina
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000155)

    expected_info = {
        # The effect of clearing the action condition when the HP drops below the threshold is omitted
        AbilityEffectInfo(
            400000155, ConditionComposite([Condition.TARGET_WATER, Condition.ON_SELF_HP_GTE_60]),
            BuffParameter.ATK_BUFF, 0.05, duration_sec=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_combo_count_threshold(transformer_ability: AbilityTransformer):
    # Summer Cleo - 10650401
    # https://dragalialost.gamepedia.com/Karina
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000489)

    expected_info = {
        # The effect of clearing the action condition when the combo counter resets is omitted
        AbilityEffectInfo(
            400000489, ConditionComposite([Condition.TARGET_LIGHT, Condition.ON_COMBO_GTE_10]),
            BuffParameter.RESISTANCE_SHADOW, 0.1, duration_sec=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_grant_shield_on_low_hp(transformer_ability: AbilityTransformer):
    # Grace - 10850503
    # https://dragalialost.gamepedia.com/Grace
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000657)

    expected_info = {
        AbilityEffectInfo(
            400000657, ConditionComposite([Condition.TARGET_SHADOW, Condition.ON_SELF_HP_LT_40]),
            BuffParameter.SHIELD_SINGLE_DMG, 0.5, duration_sec=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_elem_res_when_high_hp(transformer_ability: AbilityTransformer):
    # Forager Cleo - 10750203
    # https://dragalialost.gamepedia.com/Forager_Cleo
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000168)

    expected_info = {
        AbilityEffectInfo(
            400000168, ConditionComposite([Condition.TARGET_WATER, Condition.SELF_HP_GTE_80]),
            BuffParameter.RESISTANCE_FLAME, 0.06, duration_sec=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_combo_time_extend(transformer_ability: AbilityTransformer):
    # Nobunaga - 10250103
    # https://dragalialost.gamepedia.com/Nobunaga
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000708)

    expected_info = {
        AbilityEffectInfo(400000708, ConditionComposite(Condition.TARGET_FLAME), BuffParameter.COMBO_TIME, 2.5),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)
