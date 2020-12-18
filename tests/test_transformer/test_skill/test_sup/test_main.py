import pytest

from dlparse.enums import (BuffParameter, Condition, ConditionCategories, ConditionComposite, HitTargetSimple)
from dlparse.errors import SkillDataNotFoundError
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_skill_not_found(transformer_skill: SkillTransformer):
    with pytest.raises(SkillDataNotFoundError) as error:
        transformer_skill.transform_supportive(87)

        assert error.value.skill_id == 87


def test_single_effect_to_team(transformer_skill: SkillTransformer):
    # Kirsty S2
    # https://dragalialost.gamepedia.com/Kirsty
    skill_data_base = transformer_skill.transform_supportive(105503022)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        BuffEffectInfo("BUF_ALL_ATK_SSR_30_LV01", HitTargetSimple.TEAM, BuffParameter.ATK, 0.15, 15, 0)
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BUF_ALL_ATK_SSR_30_LV02", HitTargetSimple.TEAM, BuffParameter.ATK, 0.2, 15, 0)
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("BUF_ALL_ATK_SSR_30_LV03", HitTargetSimple.TEAM, BuffParameter.ATK, 0.25, 15, 0)
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_single_effect_to_team_limited(transformer_skill: SkillTransformer):
    # Emma S1
    # https://dragalialost.gamepedia.com/Emma
    skill_data_base = transformer_skill.transform_supportive(105401031)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        BuffEffectInfo("BUF_160_ATK_FIRE_LV01", HitTargetSimple.TEAM, BuffParameter.ATK, 0.15, 15, 0)
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BUF_160_ATK_FIRE_LV02", HitTargetSimple.TEAM, BuffParameter.ATK, 0.20, 15, 0)
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("BUF_160_ATK_FIRE_LV03", HitTargetSimple.TEAM, BuffParameter.ATK, 0.25, 15, 0)
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == set()
    assert skill_data.buffs == [set()] * skill_data_base.max_level

    # Flame-attuned (should be effective)
    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.TARGET_ELEM_FLAME))

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)

    # Water-attuned (should be ineffective)
    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.TARGET_ELEM_WATER))

    assert skill_data.max_lv_buffs == set()
    assert skill_data.buffs == [set()] * skill_data_base.max_level


def test_single_effect_area(transformer_skill: SkillTransformer):
    # Gala Euden S1
    # https://dragalialost.gamepedia.com/Gala_Prince
    skill_data_base = transformer_skill.transform_supportive(101504031)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        BuffEffectInfo("SWD_115_04_ATK_FLD_LV01", HitTargetSimple.AREA, BuffParameter.ATK, 0.10, 10, 0)
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("SWD_115_04_ATK_FLD_LV02", HitTargetSimple.AREA, BuffParameter.ATK, 0.15, 10, 0)
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("SWD_115_04_ATK_FLD_LV03", HitTargetSimple.AREA, BuffParameter.ATK, 0.20, 10, 0)
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_multi_effect_to_team(transformer_skill: SkillTransformer):
    # Patia S1
    # https://dragalialost.gamepedia.com/Patia
    skill_data_base = transformer_skill.transform_supportive(105405021)

    assert skill_data_base.max_level == 4

    expected_buffs_lv_1 = {
        BuffEffectInfo("BUF_184_DEF_LV01", HitTargetSimple.TEAM, BuffParameter.DEF, 0.15, 15, 0)
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BUF_184_DEF_LV02", HitTargetSimple.TEAM, BuffParameter.DEF, 0.2, 15, 0)
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("BUF_184_DEF_LV03", HitTargetSimple.TEAM, BuffParameter.DEF, 0.25, 15, 0)
    }
    expected_buffs_lv_4 = {
        BuffEffectInfo("BUF_184_DEF_LV04", HitTargetSimple.TEAM, BuffParameter.DEF, 0.25, 15, 0),
        BuffEffectInfo("BUF_184_ATK_LV04", HitTargetSimple.TEAM, BuffParameter.ATK, 0.15, 15, 0)
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3, expected_buffs_lv_4]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_4)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_multi_effect_to_nearby_1(transformer_skill: SkillTransformer):
    # Halloween Odetta S2
    # https://dragalialost.gamepedia.com/Halloween_Odetta
    skill_data_base = transformer_skill.transform_supportive(101402012)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        BuffEffectInfo("BUF_166_ATK_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15, 15, 0)
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BUF_166_ATK_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.20, 15, 0)
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("BUF_166_ATK_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.25, 15, 0)
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_multi_effect_to_nearby_2(transformer_skill: SkillTransformer):
    # Summer Cleo S2
    # https://dragalialost.gamepedia.com/Summer_Cleo
    skill_data_base = transformer_skill.transform_supportive(106504012)

    expected_base_buffs_lv_1 = {
        BuffEffectInfo("BOW_108_04_ATK_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.03, 10, 0),
        BuffEffectInfo("BOW_108_04_CRT_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE, 0.02, 10, 0),
        BuffEffectInfo("BOW_108_04_SKILL_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SKILL_DAMAGE,
                       0.1, 10, 99),
        BuffEffectInfo("BOW_108_04_SPB_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SP_RATE, 0.1, 10, 0),
    }
    expected_base_buffs_lv_2 = {
        BuffEffectInfo("BOW_108_04_ATK_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.05, 10, 0),
        BuffEffectInfo("BOW_108_04_CRT_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE, 0.03, 10, 0),
        BuffEffectInfo("BOW_108_04_SKILL_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SKILL_DAMAGE,
                       0.1, 10, 99),
        BuffEffectInfo("BOW_108_04_SPB_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SP_RATE, 0.1, 10, 0),
    }
    expected_base_buffs_lv_3 = {
        BuffEffectInfo("BOW_108_04_ATK_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.05, 10, 0),
        BuffEffectInfo("BOW_108_04_CRT_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE, 0.03, 10, 0),
        BuffEffectInfo("BOW_108_04_SKILL_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SKILL_DAMAGE,
                       0.1, 10, 99),
        BuffEffectInfo("BOW_108_04_SPB_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SP_RATE, 0.1, 10, 0),
    }

    on_0_plus_buffs = {
        BuffEffectInfo("BOW_108_04_DEF_LV03", HitTargetSimple.SELF, BuffParameter.DEF, 0.1, 10, 0),
    }
    on_1_plus_buffs = on_0_plus_buffs | {
        BuffEffectInfo("BOW_108_04_CRTDMG_LV03", HitTargetSimple.SELF, BuffParameter.CRT_DAMAGE, 0.1, 10, 0),
    }
    on_2_plus_buffs = on_1_plus_buffs | {
        BuffEffectInfo("BOW_108_04_SP_LV03", HitTargetSimple.SELF, BuffParameter.SP_CHARGE_PCT_S1, 1, 0, 0),
    }

    expected_base_buffs = [expected_base_buffs_lv_1, expected_base_buffs_lv_2, expected_base_buffs_lv_3]

    # arr[i][j] is the additional buffs granted, i = skill level / j = count of teammates covered
    expected_additional_buffs = [
        [set(), set(), set(), set()],
        [set(), set(), set(), set()],
        [on_0_plus_buffs, on_1_plus_buffs, on_2_plus_buffs, on_2_plus_buffs]
    ]

    assert skill_data_base.max_level == 3

    for cond_enum, teammate_count in ConditionCategories.skill_teammates_covered.conversion_dict.items():
        skill_data = skill_data_base.with_conditions(ConditionComposite(cond_enum))

        check_buff_unit_match(skill_data.max_lv_buffs,
                              expected_base_buffs_lv_3 | expected_additional_buffs[-1][teammate_count])

        for skill_lv in range(skill_data_base.max_level):
            actual_buffs = skill_data.buffs[skill_lv]
            expected_buffs = expected_base_buffs[skill_lv] | expected_additional_buffs[skill_lv][teammate_count]

            check_buff_unit_match(actual_buffs, expected_buffs)


def test_has_phase_1(transformer_skill: SkillTransformer):
    # Summer Julietta S2 - P1
    # https://dragalialost.gamepedia.com/Summer_Julietta
    skill_data_base = transformer_skill.transform_supportive(104502012)

    expected_buffs_lv_1 = {
        BuffEffectInfo("AXE_107_04_ATK_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15, 15, 0),
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("AXE_107_04_ATK_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15, 15, 0),
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("AXE_107_04_ATK_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15, 15, 0),
    }

    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_has_phase_2(transformer_skill: SkillTransformer):
    # Summer Julietta S2 - P2
    # https://dragalialost.gamepedia.com/Summer_Julietta
    skill_data_base = transformer_skill.transform_supportive(104502013)

    expected_base_buffs_lv_1 = {
        BuffEffectInfo("AXE_107_04_ATK_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15, 15, 0),
    }
    expected_base_buffs_lv_2 = {
        BuffEffectInfo("AXE_107_04_ATK_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15, 15, 0),
    }
    expected_base_buffs_lv_3 = {
        BuffEffectInfo("AXE_107_04_ATK_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15, 15, 0),
    }

    addl_buffs = [
        {
            BuffEffectInfo("AXE_107_04_CRT_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE,
                           0.08, 15, 0),
        },
        {
            BuffEffectInfo("AXE_107_04_CRT_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE,
                           0.1, 15, 0),
        },
        {
            BuffEffectInfo("AXE_107_04_CRT_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE,
                           0.13, 15, 0),
        }
    ]

    expected_base_buffs = [expected_base_buffs_lv_1, expected_base_buffs_lv_2, expected_base_buffs_lv_3]

    assert skill_data_base.max_level == 3

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_base_buffs_lv_3 | addl_buffs[-1])

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv] | addl_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_has_phase_3(transformer_skill: SkillTransformer):
    # Summer Julietta S2 - P3
    # https://dragalialost.gamepedia.com/Summer_Julietta
    skill_data_base = transformer_skill.transform_supportive(104502014)

    expected_base_buffs_lv_1 = {
        BuffEffectInfo("AXE_107_04_ATK_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15, 15, 0),
    }
    expected_base_buffs_lv_2 = {
        BuffEffectInfo("AXE_107_04_ATK_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15, 15, 0),
    }
    expected_base_buffs_lv_3 = {
        BuffEffectInfo("AXE_107_04_ATK_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15, 15, 0),
    }

    addl_buffs = [
        {
            BuffEffectInfo("AXE_107_04_CRT_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE,
                           0.08, 15, 0),
            BuffEffectInfo("AXE_107_04_SLD_LV01", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SHIELD_SINGLE_DMG,
                           0.2, 0, 1),
        },
        {
            BuffEffectInfo("AXE_107_04_CRT_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE,
                           0.1, 15, 0),
            BuffEffectInfo("AXE_107_04_SLD_LV02", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SHIELD_SINGLE_DMG,
                           0.3, 0, 1),
        },
        {
            BuffEffectInfo("AXE_107_04_CRT_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE,
                           0.13, 15, 0),
            BuffEffectInfo("AXE_107_04_SLD_LV03", HitTargetSimple.SELF_SURROUNDING, BuffParameter.SHIELD_SINGLE_DMG,
                           0.4, 0, 1),
        }
    ]

    expected_base_buffs = [expected_base_buffs_lv_1, expected_base_buffs_lv_2, expected_base_buffs_lv_3]

    assert skill_data_base.max_level == 3

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_base_buffs_lv_3 | addl_buffs[-1])

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv] | addl_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_with_attack(transformer_skill: SkillTransformer):
    # Marth S2 - P3
    # https://dragalialost.gamepedia.com/Marth
    skill_data_base = transformer_skill.transform_supportive(101501024)

    expected_buffs_lv_1 = {
        BuffEffectInfo("SWD_107_04_ALL_SPD_LV01", HitTargetSimple.TEAM, BuffParameter.ATK_SPD, 0.2, 10, 0),
        BuffEffectInfo("SWD_107_04_ALL_ATK_LV01", HitTargetSimple.TEAM, BuffParameter.ATK, 0.1, 10, 0),
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("SWD_107_04_ALL_SPD_LV02", HitTargetSimple.TEAM, BuffParameter.ATK_SPD, 0.3, 10, 0),
        BuffEffectInfo("SWD_107_04_ALL_ATK_LV02", HitTargetSimple.TEAM, BuffParameter.ATK, 0.1, 10, 0),
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("SWD_107_04_ALL_SPD_LV03", HitTargetSimple.TEAM, BuffParameter.ATK_SPD, 0.3, 10, 0),
        BuffEffectInfo("SWD_107_04_ALL_ATK_LV03", HitTargetSimple.TEAM, BuffParameter.ATK, 0.1, 10, 0),
    }

    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_with_attack_one_time_use(transformer_skill: SkillTransformer):
    # Lazry S1 @ High Power
    # https://dragalialost.gamepedia.com/Lazry
    skill_data_base = transformer_skill.transform_supportive(104502033)

    expected_buffs_lv_1 = {
        BuffEffectInfo("AXE_117_04_PLUS_BUF_LV01", HitTargetSimple.SELF, BuffParameter.SKILL_DAMAGE, 0.2, 0, 1),
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("AXE_117_04_PLUS_BUF_LV02", HitTargetSimple.SELF, BuffParameter.SKILL_DAMAGE, 0.2, 0, 1),
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("AXE_117_04_PLUS_BUF_LV03", HitTargetSimple.SELF, BuffParameter.SKILL_DAMAGE, 0.2, 0, 1),
    }

    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_elemental_resistances(transformer_skill: SkillTransformer):
    # Pecorine S1
    # https://dragalialost.gamepedia.com/Pecorine
    skill_data_base = transformer_skill.transform_supportive(101504041)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        BuffEffectInfo("SWD_127_04_BUF_LV01", HitTargetSimple.SELF, BuffParameter.RESISTANCE_SHADOW, 0.05, 10, 0)
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("SWD_127_04_BUF_LV02", HitTargetSimple.SELF, BuffParameter.RESISTANCE_SHADOW, 0.08, 10, 0)
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("SWD_127_04_BUF_LV03", HitTargetSimple.SELF, BuffParameter.RESISTANCE_SHADOW, 0.1, 10, 0)
    }

    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_hp_drain():
    # Yue S2
    # https://dragalialost.gamepedia.com/Yue
    pass  # TEST: TBA - Yue S2


def test_self_debuff():
    pass  # TEST: TBA - Durant S2 / Yue S2
