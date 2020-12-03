import pytest

from dlparse.enums import (
    BuffParameter, HitTargetSimple, SkillCondition, SkillConditionComposite, SkillConditionCategories
)
from dlparse.errors import SkillDataNotFoundError
from dlparse.model import SupportiveSkillUnit
from dlparse.transformer import SkillTransformer


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
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_ATK_SSR_30_LV01",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.20,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_ATK_SSR_30_LV02",
            action_cond_id=302030401,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.25,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_ATK_SSR_30_LV03",
            action_cond_id=302030501,
            max_stack_count=0
        ),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    # No element given

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_buffs_lv_3

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_single_effect_to_team_limited(transformer_skill: SkillTransformer):
    # Emma S1
    # https://dragalialost.gamepedia.com/Emma
    skill_data_base = transformer_skill.transform_supportive(105401031)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_160_ATK_FIRE_LV01",
            action_cond_id=165,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.20,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_160_ATK_FIRE_LV02",
            action_cond_id=166,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.25,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_160_ATK_FIRE_LV03",
            action_cond_id=167,
            max_stack_count=0
        ),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    # No element given

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == set()
    assert skill_data.buffs == [set()] * skill_data_base.max_level

    # Fire element given

    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_ELEM_FLAME))

    assert skill_data.max_lv_buffs == expected_buffs_lv_3
    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)

    # Wrong element given

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == set()
    assert skill_data.buffs == [set()] * skill_data_base.max_level


def test_single_effect_area(transformer_skill: SkillTransformer):
    # Gala Euden S1
    # https://dragalialost.gamepedia.com/Gala_Prince
    skill_data_base = transformer_skill.transform_supportive(101504031)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.AREA,
            parameter=BuffParameter.ATK,
            rate=0.10,
            duration_time=10,
            duration_count=0,
            hit_attr_label="SWD_115_04_ATK_FLD_LV01",
            action_cond_id=136,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.AREA,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=10,
            duration_count=0,
            hit_attr_label="SWD_115_04_ATK_FLD_LV02",
            action_cond_id=137,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.AREA,
            parameter=BuffParameter.ATK,
            rate=0.20,
            duration_time=10,
            duration_count=0,
            hit_attr_label="SWD_115_04_ATK_FLD_LV03",
            action_cond_id=138,
            max_stack_count=0
        ),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    for skill_lv in range(skill_data_base.max_level):
        skill_data = skill_data_base.with_conditions()

        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_multi_effect_to_team(transformer_skill: SkillTransformer):
    # Patia S1
    # https://dragalialost.gamepedia.com/Patia
    skill_data_base = transformer_skill.transform_supportive(105405021)

    assert skill_data_base.max_level == 4

    expected_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.DEF,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_184_DEF_LV01",
            action_cond_id=303030201,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.DEF,
            rate=0.20,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_184_DEF_LV02",
            action_cond_id=303030301,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.DEF,
            rate=0.25,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_184_DEF_LV03",
            action_cond_id=303030401,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_4 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.DEF,
            rate=0.25,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_184_DEF_LV04",
            action_cond_id=303030401,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_184_ATK_LV04",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3, expected_buffs_lv_4]

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_buffs_lv_4
    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_multi_effect_to_nearby_1(transformer_skill: SkillTransformer):
    # Halloween Odetta S2
    # https://dragalialost.gamepedia.com/Halloween_Odetta
    skill_data_base = transformer_skill.transform_supportive(101402012)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_166_ATK_LV01",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.20,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_166_ATK_LV02",
            action_cond_id=302030401,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.25,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_166_ATK_LV03",
            action_cond_id=302030501,
            max_stack_count=0
        ),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_buffs_lv_3
    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_multi_effect_to_nearby_2(transformer_skill: SkillTransformer):
    # Summer Cleo S2
    # https://dragalialost.gamepedia.com/Summer_Cleo
    skill_data_base = transformer_skill.transform_supportive(106504012)

    expected_base_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.03,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_ATK_LV01",
            action_cond_id=193,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.CRT_RATE,
            rate=0.02,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_CRT_LV01",
            action_cond_id=37,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SKILL_DAMAGE,
            rate=0.1,
            duration_time=10,
            duration_count=99,
            hit_attr_label="BOW_108_04_SKILL_LV01",
            action_cond_id=197,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SP_RATE,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_SPB_LV01",
            action_cond_id=194,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.05,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_ATK_LV02",
            action_cond_id=76,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.CRT_RATE,
            rate=0.03,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_CRT_LV02",
            action_cond_id=38,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SKILL_DAMAGE,
            rate=0.1,
            duration_time=10,
            duration_count=99,
            hit_attr_label="BOW_108_04_SKILL_LV02",
            action_cond_id=197,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SP_RATE,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_SPB_LV02",
            action_cond_id=194,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.05,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_ATK_LV03",
            action_cond_id=76,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.CRT_RATE,
            rate=0.03,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_CRT_LV03",
            action_cond_id=38,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SKILL_DAMAGE,
            rate=0.1,
            duration_time=10,
            duration_count=99,
            hit_attr_label="BOW_108_04_SKILL_LV03",
            action_cond_id=197,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SP_RATE,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_SPB_LV03",
            action_cond_id=194,
            max_stack_count=0
        ),
    }

    on_0_plus_buffs = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.DEF,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_DEF_LV03",
            action_cond_id=303020101,
            max_stack_count=0
        )
    }
    on_1_plus_buffs = on_0_plus_buffs | {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.CRT_DAMAGE,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_CRTDMG_LV03",
            action_cond_id=1176,
            max_stack_count=0
        )
    }
    on_2_plus_buffs = on_1_plus_buffs | {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.SP_CHARGE_PCT_S1,
            rate=1,
            duration_time=0,
            duration_count=0,
            hit_attr_label="BOW_108_04_SP_LV03",
            action_cond_id=0,
            max_stack_count=0
        )
    }

    expected_base_buffs = [expected_base_buffs_lv_1, expected_base_buffs_lv_2, expected_base_buffs_lv_3]

    # arr[i][j] is the additional buffs granted, i = skill level / j = count of teammates covered
    expected_additional_buffs = [
        [set(), set(), set(), set()],
        [set(), set(), set(), set()],
        [on_0_plus_buffs, on_1_plus_buffs, on_2_plus_buffs, on_2_plus_buffs]
    ]

    assert skill_data_base.max_level == 3

    for cond_enum, teammate_count in SkillConditionCategories.skill_teammates_covered.conversion_dict.items():
        skill_data = skill_data_base.with_conditions(SkillConditionComposite(cond_enum))

        assert skill_data.max_lv_buffs == expected_base_buffs_lv_3 | expected_additional_buffs[-1][teammate_count]
        for skill_lv in range(skill_data_base.max_level):
            expected_buffs = expected_base_buffs[skill_lv] | expected_additional_buffs[skill_lv][teammate_count]
            actual_buffs = skill_data.buffs[skill_lv]

            assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_has_phase_1(transformer_skill: SkillTransformer):
    # Summer Julietta S2 - P1
    # https://dragalialost.gamepedia.com/Summer_Julietta
    skill_data_base = transformer_skill.transform_supportive(104502012)

    expected_base_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="AXE_107_04_ATK_LV01",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="AXE_107_04_ATK_LV02",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="AXE_107_04_ATK_LV03",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }

    expected_base_buffs = [expected_base_buffs_lv_1, expected_base_buffs_lv_2, expected_base_buffs_lv_3]

    assert skill_data_base.max_level == 3

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_base_buffs_lv_3
    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_has_phase_2(transformer_skill: SkillTransformer):
    # Summer Julietta S2 - P2
    # https://dragalialost.gamepedia.com/Summer_Julietta
    skill_data_base = transformer_skill.transform_supportive(104502013)

    expected_base_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="AXE_107_04_ATK_LV01",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="AXE_107_04_ATK_LV02",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="AXE_107_04_ATK_LV03",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }

    addl_buffs = [
        {
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF_SURROUNDING,
                parameter=BuffParameter.CRT_RATE,
                rate=0.08,
                duration_time=15,
                duration_count=0,
                hit_attr_label="AXE_107_04_CRT_LV01",
                action_cond_id=157,
                max_stack_count=0
            )
        },
        {
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF_SURROUNDING,
                parameter=BuffParameter.CRT_RATE,
                rate=0.10,
                duration_time=15,
                duration_count=0,
                hit_attr_label="AXE_107_04_CRT_LV02",
                action_cond_id=158,
                max_stack_count=0
            )
        },
        {
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF_SURROUNDING,
                parameter=BuffParameter.CRT_RATE,
                rate=0.13,
                duration_time=15,
                duration_count=0,
                hit_attr_label="AXE_107_04_CRT_LV03",
                action_cond_id=572,
                max_stack_count=0
            )
        }
    ]

    expected_base_buffs = [expected_base_buffs_lv_1, expected_base_buffs_lv_2, expected_base_buffs_lv_3]

    assert skill_data_base.max_level == 3

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_base_buffs_lv_3 | addl_buffs[-1]
    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv] | addl_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_has_phase_3(transformer_skill: SkillTransformer):
    # Summer Julietta S2 - P3
    # https://dragalialost.gamepedia.com/Summer_Julietta
    skill_data_base = transformer_skill.transform_supportive(104502014)

    expected_base_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="AXE_107_04_ATK_LV01",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="AXE_107_04_ATK_LV02",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="AXE_107_04_ATK_LV03",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }

    addl_buffs = [
        {
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF_SURROUNDING,
                parameter=BuffParameter.SHIELD_SINGLE_DMG,
                rate=0.2,
                duration_time=0,
                duration_count=1,
                hit_attr_label="AXE_107_04_SLD_LV01",
                action_cond_id=316010401,
                max_stack_count=1
            ),
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF_SURROUNDING,
                parameter=BuffParameter.CRT_RATE,
                rate=0.08,
                duration_time=15,
                duration_count=0,
                hit_attr_label="AXE_107_04_CRT_LV01",
                action_cond_id=157,
                max_stack_count=0
            )
        },
        {
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF_SURROUNDING,
                parameter=BuffParameter.SHIELD_SINGLE_DMG,
                rate=0.3,
                duration_time=0,
                duration_count=1,
                hit_attr_label="AXE_107_04_SLD_LV02",
                action_cond_id=316010501,
                max_stack_count=1
            ),
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF_SURROUNDING,
                parameter=BuffParameter.CRT_RATE,
                rate=0.10,
                duration_time=15,
                duration_count=0,
                hit_attr_label="AXE_107_04_CRT_LV02",
                action_cond_id=158,
                max_stack_count=0
            )
        },
        {
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF_SURROUNDING,
                parameter=BuffParameter.SHIELD_SINGLE_DMG,
                rate=0.4,
                duration_time=0,
                duration_count=1,
                hit_attr_label="AXE_107_04_SLD_LV03",
                action_cond_id=316010601,
                max_stack_count=1
            ),
            SupportiveSkillUnit(
                target=HitTargetSimple.SELF_SURROUNDING,
                parameter=BuffParameter.CRT_RATE,
                rate=0.13,
                duration_time=15,
                duration_count=0,
                hit_attr_label="AXE_107_04_CRT_LV03",
                action_cond_id=572,
                max_stack_count=0
            )
        }
    ]

    expected_base_buffs = [expected_base_buffs_lv_1, expected_base_buffs_lv_2, expected_base_buffs_lv_3]

    assert skill_data_base.max_level == 3

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_base_buffs_lv_3 | addl_buffs[-1]
    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv] | addl_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_with_attack(transformer_skill: SkillTransformer):
    # Marth S2 - P3
    # https://dragalialost.gamepedia.com/Marth
    skill_data_base = transformer_skill.transform_supportive(101501024)

    expected_base_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK_SPD,
            rate=0.2,
            duration_time=10,
            duration_count=0,
            hit_attr_label="SWD_107_04_ALL_SPD_LV01",
            action_cond_id=312010201,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="SWD_107_04_ALL_ATK_LV01",
            action_cond_id=302020101,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK_SPD,
            rate=0.3,
            duration_time=10,
            duration_count=0,
            hit_attr_label="SWD_107_04_ALL_SPD_LV02",
            action_cond_id=89,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="SWD_107_04_ALL_ATK_LV02",
            action_cond_id=302020101,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK_SPD,
            rate=0.3,
            duration_time=10,
            duration_count=0,
            hit_attr_label="SWD_107_04_ALL_SPD_LV03",
            action_cond_id=89,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="SWD_107_04_ALL_ATK_LV03",
            action_cond_id=302020101,
            max_stack_count=0
        ),
    }

    expected_base_buffs = [expected_base_buffs_lv_1, expected_base_buffs_lv_2, expected_base_buffs_lv_3]

    assert skill_data_base.max_level == 3

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_base_buffs_lv_3
    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_with_attack_one_time_use(transformer_skill: SkillTransformer):
    # Lazry S1 @ High Power
    # https://dragalialost.gamepedia.com/Lazry
    skill_data_base = transformer_skill.transform_supportive(104502033)

    expected_base_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.SKILL_DAMAGE,
            rate=0.2,
            duration_time=0,
            duration_count=1,
            hit_attr_label="AXE_117_04_PLUS_BUF_LV01",
            action_cond_id=787,
            max_stack_count=0
        ),
    }
    expected_base_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.SKILL_DAMAGE,
            rate=0.2,
            duration_time=0,
            duration_count=1,
            hit_attr_label="AXE_117_04_PLUS_BUF_LV02",
            action_cond_id=787,
            max_stack_count=1
        ),
    }
    expected_base_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.SKILL_DAMAGE,
            rate=0.2,
            duration_time=0,
            duration_count=1,
            hit_attr_label="AXE_117_04_PLUS_BUF_LV03",
            action_cond_id=787,
            max_stack_count=1
        ),
    }

    expected_base_buffs = [expected_base_buffs_lv_1, expected_base_buffs_lv_2, expected_base_buffs_lv_3]

    assert skill_data_base.max_level == 3

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_base_buffs_lv_3
    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_hp_drain(transformer_skill: SkillTransformer):
    # Yue S2
    # https://dragalialost.gamepedia.com/Yue
    pass  # TEST: TBA - Yue S2
