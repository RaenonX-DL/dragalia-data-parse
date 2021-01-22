from dlparse.enums import BuffParameter, Condition, ConditionComposite
from dlparse.transformer import AbilityTransformer
from tests.utils import AbilityEffectInfo, check_ability_effect_unit_match


def test_od_punisher(transformer_ability: AbilityTransformer):
    # Seimei - 10750104
    # https://dragalialost.gamepedia.com/Seimei
    ex_ability_data = transformer_ability.transform_ex_ability(106000008)

    expected_info = {
        AbilityEffectInfo(
            106000008, ConditionComposite(Condition.TARGET_OD_STATE),
            BuffParameter.OD_GAUGE_DAMAGE, 0.10, max_occurrences=1
        ),
        AbilityEffectInfo(
            106000008, ConditionComposite(Condition.TARGET_OD_STATE),
            BuffParameter.OD_STATE_PUNISHER, 0.15, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_debuffed_punisher(transformer_ability: AbilityTransformer):
    # Gala Leif - 10150303
    # https://dragalialost.gamepedia.com/Gala_Leif
    ex_ability_data = transformer_ability.transform_ex_ability(106080008)

    expected_info = {
        AbilityEffectInfo(
            106080008, ConditionComposite(Condition.TARGET_ATK_OR_DEF_DOWN),
            BuffParameter.ATK_OR_DEF_DOWN_PUNISHER, 0.08, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_paralyzed_punisher(transformer_ability: AbilityTransformer):
    # Sharena - 10550404
    # https://dragalialost.gamepedia.com/Sharena
    ex_ability_data = transformer_ability.transform_ex_ability(120040008)

    expected_info = {
        AbilityEffectInfo(
            120040008, ConditionComposite(),
            BuffParameter.PARALYZED_PUNISHER, 0.08, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_auto_dmg_up(transformer_ability: AbilityTransformer):
    # Gala Laxi - 10350102
    # https://dragalialost.gamepedia.com/Gala_Laxi
    ex_ability_data = transformer_ability.transform_ex_ability(106070008)

    expected_info = {
        AbilityEffectInfo(
            106070008, ConditionComposite(),
            BuffParameter.AUTO_DAMAGE, 0.2, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_fs_dmg_up(transformer_ability: AbilityTransformer):
    # Grace - 10850503
    # https://dragalialost.gamepedia.com/Grace
    ex_ability_data = transformer_ability.transform_ex_ability(106000016)

    expected_info = {
        AbilityEffectInfo(
            106000016, ConditionComposite(),
            BuffParameter.FS_DAMAGE, 0.2, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_crt_dmg_up(transformer_ability: AbilityTransformer):
    # Halloween Mym - 10450102
    # https://dragalialost.gamepedia.com/Halloween_Mym
    ex_ability_data = transformer_ability.transform_ex_ability(126000008)

    expected_info = {
        AbilityEffectInfo(
            126000008, ConditionComposite(),
            BuffParameter.CRT_DAMAGE, 0.3, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_light_dmg_up(transformer_ability: AbilityTransformer):
    # Peony - 10750402
    # https://dragalialost.gamepedia.com/Peony
    ex_ability_data = transformer_ability.transform_ex_ability(157570408)

    expected_info = {
        AbilityEffectInfo(
            157570408, ConditionComposite(),
            BuffParameter.LIGHT_ELEM_DMG_UP, 0.2, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_hp_and_def(transformer_ability: AbilityTransformer):
    # Chrom - 10150105
    # https://dragalialost.gamepedia.com/Chrom
    ex_ability_data = transformer_ability.transform_ex_ability(101060010)

    expected_info = {
        AbilityEffectInfo(
            101060010, ConditionComposite(),
            BuffParameter.DEF_PASSIVE, 0.1, max_occurrences=1
        ),
        AbilityEffectInfo(
            101060010, ConditionComposite(),
            BuffParameter.HP_RAISE_BY_MAX, 0.1, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_hp_on_revival(transformer_ability: AbilityTransformer):
    # Kimono Elisanne - 10550103
    # https://dragalialost.gamepedia.com/Kimono_Elisanne
    ex_ability_data = transformer_ability.transform_ex_ability(166000008)

    expected_info = {
        AbilityEffectInfo(
            166000008, ConditionComposite(Condition.ON_SELF_REVIVED),
            BuffParameter.HEAL_MAX_HP, 0.3, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_shapeshifting_boost(transformer_ability: AbilityTransformer):
    # Gala Euden - 10150403
    # https://dragalialost.gamepedia.com/Gala_Euden
    ex_ability_data = transformer_ability.transform_ex_ability(136000008)

    expected_info = {
        AbilityEffectInfo(
            136000008, ConditionComposite(),
            BuffParameter.DRAGON_DAMAGE, 0.1, max_occurrences=1
        ),
        AbilityEffectInfo(
            136000008, ConditionComposite(),
            BuffParameter.DRAGON_TIME, 0.2, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)


def test_buff_time(transformer_ability: AbilityTransformer):
    # Tobias
    # https://dragalialost.gamepedia.com/Tobias
    ex_ability_data = transformer_ability.transform_ex_ability(118000008)

    expected_info = {
        AbilityEffectInfo(
            118000008, ConditionComposite(),
            BuffParameter.TARGETED_BUFF_TIME, 0.2, max_occurrences=1
        ),
    }

    check_ability_effect_unit_match(ex_ability_data.effect_units, expected_info)
