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


def test_fs_dmg_up_on_got_hit(transformer_ability: AbilityTransformer):
    # MH Berserk - 10150104
    # https://dragalialost.gamepedia.com/Hunter_Berserker
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000706)

    expected_info = {
        AbilityEffectInfo(
            400000706, ConditionComposite([Condition.TARGET_FLAME, Condition.ON_HIT]),
            BuffParameter.FS_DAMAGE_BUFF, 0.2, duration_count=1,
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_atk_up_on_hp_above(transformer_ability: AbilityTransformer):
    # Original Karina - 10440201
    # https://dragalialost.gamepedia.com/Karina
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000155)

    expected_info = {
        # The effect of clearing the action condition when the HP drops below the threshold is omitted
        AbilityEffectInfo(
            400000155, ConditionComposite([Condition.TARGET_WATER, Condition.ON_HP_GTE_60]),
            BuffParameter.ATK_BUFF, 0.05, duration_sec=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_atk_up_on_hp_below(transformer_ability: AbilityTransformer):
    # Emma - 10540103
    # https://dragalialost.gamepedia.com/Emma
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000017)

    expected_info = {
        # The effect of clearing the action condition when the HP drops below the threshold is omitted
        AbilityEffectInfo(
            400000017, ConditionComposite([Condition.TARGET_FLAME, Condition.ON_HP_LT_40]),
            BuffParameter.ATK_BUFF, 0.14, duration_sec=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_atk_up_on_healed(transformer_ability: AbilityTransformer):
    # Dragonyule Lily - 10850202
    # https://dragalialost.gamepedia.com/Dragonyule_Lily
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000828)

    expected_info = {
        AbilityEffectInfo(
            400000828, ConditionComposite([Condition.TARGET_WATER, Condition.ON_HEALED]),
            BuffParameter.ATK_BUFF, 0.08, duration_sec=15, cooldown_sec=10
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_atk_up_on_dodged(transformer_ability: AbilityTransformer):
    # Yoshitsune - 10950202
    # https://dragalialost.gamepedia.com/Yoshitsune
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000853)

    expected_info = {
        AbilityEffectInfo(
            400000853, ConditionComposite([Condition.TARGET_WATER, Condition.ON_DODGE_SUCCESS]),
            BuffParameter.ATK_BUFF, 0.1, duration_sec=15, cooldown_sec=15
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_atk_up_by_dragons_claws(transformer_ability: AbilityTransformer):
    # Gala Mym - 10550101
    # https://dragalialost.gamepedia.com/Gala_Mym
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000012)

    expected_info = {
        AbilityEffectInfo(
            400000012, ConditionComposite([Condition.TARGET_FLAME, Condition.SELF_SHAPESHIFTED_1_TIME]),
            BuffParameter.ATK_BUFF, 0.1
        ),
        AbilityEffectInfo(
            400000012, ConditionComposite([Condition.TARGET_FLAME, Condition.SELF_SHAPESHIFTED_2_TIMES]),
            BuffParameter.ATK_BUFF, 0.1
        ),
        AbilityEffectInfo(
            400000012, ConditionComposite([Condition.TARGET_FLAME, Condition.SELF_SHAPESHIFTED_3_TIMES]),
            BuffParameter.ATK_BUFF, 0.15
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_grant_shield_upon_hp_below(transformer_ability: AbilityTransformer):
    # Grace - 10850503
    # https://dragalialost.gamepedia.com/Grace
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000657)

    expected_info = {
        AbilityEffectInfo(
            400000657, ConditionComposite([Condition.TARGET_SHADOW, Condition.ON_HP_LT_40]),
            BuffParameter.SHIELD_SINGLE_DMG, 0.5, duration_sec=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_elem_res_when_hp_above(transformer_ability: AbilityTransformer):
    # Forager Cleo - 10750203
    # https://dragalialost.gamepedia.com/Forager_Cleo
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000168)

    expected_info = {
        AbilityEffectInfo(
            400000168, ConditionComposite([Condition.TARGET_WATER, Condition.SELF_HP_GTE_80]),
            BuffParameter.RESISTANCE_FLAME_PASSIVE, 0.06, duration_sec=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_elem_res_on_energy_level_up(transformer_ability: AbilityTransformer):
    # Elias - 10640403
    # https://dragalialost.gamepedia.com/Elias
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000751)

    expected_info = {
        AbilityEffectInfo(
            400000751, ConditionComposite([Condition.TARGET_LIGHT, Condition.ON_ENERGY_LV_UP]),
            BuffParameter.RESISTANCE_SHADOW_BUFF, 0.07, duration_sec=15, cooldown_sec=15
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_elem_res_on_combo_count_above(transformer_ability: AbilityTransformer):
    # Summer Cleo - 10650401
    # https://dragalialost.gamepedia.com/Karina
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000489)

    expected_info = {
        # The effect of clearing the action condition when the combo counter resets is omitted
        AbilityEffectInfo(
            400000489, ConditionComposite([Condition.TARGET_LIGHT, Condition.ON_COMBO_GTE_10]),
            BuffParameter.RESISTANCE_SHADOW_BUFF, 0.1, duration_sec=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_elem_res_in_buff_field(transformer_ability: AbilityTransformer):
    # Opera Karina - 10650504
    # https://dragalialost.gamepedia.com/Opera_Karina
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000799)

    expected_info = {
        # The effect of clearing the action condition when leaving the buff field is omitted
        AbilityEffectInfo(
            400000799, ConditionComposite([Condition.TARGET_SHADOW, Condition.ON_ENTERED_BUFF_FIELD]),
            BuffParameter.RESISTANCE_LIGHT_BUFF, 0.07, duration_sec=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_atk_up_in_buff_field(transformer_ability: AbilityTransformer):
    # Dragonyule Victor S2
    # https://dragalialost.gamepedia.com/Dragonyule_Victor
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000833)

    expected_info = {
        AbilityEffectInfo(
            400000833, ConditionComposite([Condition.TARGET_SHADOW, Condition.ON_ENTERED_BUFF_FIELD]),
            BuffParameter.ATK_BUFF, 0.13
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_shadowblight_punisher_in_buff_field(transformer_ability: AbilityTransformer):
    # Gala Chelle
    # https://dragalialost.gamepedia.com/Gala_Chelle (404 as of 2020/01/29)
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000858)

    expected_info = {
        AbilityEffectInfo(
            400000858, ConditionComposite([Condition.TARGET_SHADOW, Condition.ON_ENTERED_BUFF_FIELD]),
            BuffParameter.SHADOWBLIGHTED_PUNISHER, 0.08
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_crt_up_by_combo_count(transformer_ability: AbilityTransformer):
    # Kimono Elisanne - 10550103
    # https://dragalialost.gamepedia.com/Kimono_Elisanne
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000838)

    expected_info = {
        AbilityEffectInfo(
            400000838, ConditionComposite([Condition.TARGET_FLAME, Condition.ON_COMBO_DIV_BY_10]),
            BuffParameter.CRT_RATE_PASSIVE, 0.01, max_stack_count=20
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_fill_dragon_gauge_by_combo_count(transformer_ability: AbilityTransformer):
    # Gala Leonidas - 10950101
    # https://dragalialost.gamepedia.com/Gala_Leonidas
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000823)

    expected_info = {
        # The effect of clearing the action condition when the combo counter resets is omitted
        AbilityEffectInfo(
            400000823, ConditionComposite([Condition.TARGET_FLAME, Condition.ON_COMBO_DIV_BY_50]),
            BuffParameter.DRAGON_GAUGE_FILL, 0.03
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_energy_level_up_by_combo_count(transformer_ability: AbilityTransformer):
    # Gala Sarisse - 10650101
    # https://dragalialost.gamepedia.com/Gala_Sarisse
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000709)

    expected_info = {
        # The effect of clearing the action condition when the combo counter resets is omitted
        AbilityEffectInfo(
            400000709, ConditionComposite([Condition.TARGET_FLAME, Condition.ON_COMBO_DIV_BY_20]),
            BuffParameter.ENERGY_LEVEL, 1, duration_count=0, max_stack_count=0
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_inspire_level_up_on_energy_level_up(transformer_ability: AbilityTransformer):
    # Lucretia - 10750401
    # https://dragalialost.gamepedia.com/Lucretia
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000541)

    expected_info = {
        AbilityEffectInfo(
            400000541, ConditionComposite([Condition.TARGET_LIGHT, Condition.ON_ENERGY_LV_UP]),
            BuffParameter.INSPIRE_LEVEL, 1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_inspire_level_up_on_energy_level_up_prob(transformer_ability: AbilityTransformer):
    # Lucretia - 10750401 (CEX Lv4)
    # https://dragalialost.gamepedia.com/Lucretia
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000539)

    expected_info = {
        AbilityEffectInfo(
            400000539, ConditionComposite([Condition.TARGET_LIGHT, Condition.ON_ENERGY_LV_UP]),
            BuffParameter.INSPIRE_LEVEL, 1, probability=80
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_infliction_rate_up(transformer_ability: AbilityTransformer):
    # Delphi - 10350502
    # https://dragalialost.gamepedia.com/Delphi
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000627)

    expected_info = {
        # The effect of clearing the action condition when the combo counter resets is omitted
        AbilityEffectInfo(
            400000627, ConditionComposite([Condition.TARGET_SHADOW]), BuffParameter.INFLICT_PROB_POISON, 0.5
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


def test_regen_on_hp_below(transformer_ability: AbilityTransformer):
    # Lea - 10150103
    # https://dragalialost.gamepedia.com/Nobunaga
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000710)

    expected_info = {
        AbilityEffectInfo(
            400000710, ConditionComposite([Condition.TARGET_FLAME, Condition.ON_HP_LT_60]),
            BuffParameter.HEAL_OVER_TIME_HP, 0.04, duration_sec=20, slip_interval_sec=3.9
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_regen_on_combo_above(transformer_ability: AbilityTransformer):
    # Summer Norwin - 10350302
    # https://dragalialost.gamepedia.com/Summer_Norwin
    ex_ability_data = transformer_ability.transform_chained_ex_ability(400000770)

    expected_info = {
        AbilityEffectInfo(
            400000770, ConditionComposite([Condition.TARGET_WIND, Condition.ON_COMBO_GTE_10]),
            BuffParameter.HEAL_OVER_TIME_RP, 0.07200000000000001, slip_interval_sec=2.9
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)
