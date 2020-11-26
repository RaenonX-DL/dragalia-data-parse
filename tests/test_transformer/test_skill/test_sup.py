import pytest

from dlparse.enums import BuffParameter, HitTargetSimple, SkillCondition, SkillConditionComposite
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
    skill_data = transformer_skill.transform_supportive(105503022)

    # TEST: TBA - Kirsty S2


def test_single_effect_to_team_limited(transformer_skill: SkillTransformer):
    # Emma S1
    # https://dragalialost.gamepedia.com/Emma
    skill_data = transformer_skill.transform_supportive(105401031)

    # TEST: TBA - Emma S1


def test_single_effect_area(transformer_skill: SkillTransformer):
    # Wedding Elisanne S1
    # https://dragalialost.gamepedia.com/Wedding_Elisanne
    # skill_data = transformer_skill.transform_supportive(101503021)
    pass

    # TEST: TBA - W!Elisanne S1


def test_multi_effect_to_team(transformer_skill: SkillTransformer):
    # Patia S1
    # https://dragalialost.gamepedia.com/Patia
    skill_data = transformer_skill.transform_supportive(105405021)

    # TEST: TBA - S!Patia S1


def test_multi_effect_to_nearby_1(transformer_skill: SkillTransformer):
    # Halloween Odetta S2
    # https://dragalialost.gamepedia.com/Halloween_Odetta
    skill_data = transformer_skill.transform_supportive(101402012)

    # TEST: TBA - H!Odetta S2


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
            action_cond_id=193
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.CRT_RATE,
            rate=0.02,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_CRT_LV01",
            action_cond_id=37
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SKILL_DAMAGE,
            rate=0.1,
            duration_time=10,
            duration_count=99,
            hit_attr_label="BOW_108_04_SKILL_LV01",
            action_cond_id=197
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SP_RATE,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_SPB_LV01",
            action_cond_id=194
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
            action_cond_id=76
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.CRT_RATE,
            rate=0.03,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_CRT_LV02",
            action_cond_id=38
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SKILL_DAMAGE,
            rate=0.1,
            duration_time=10,
            duration_count=99,
            hit_attr_label="BOW_108_04_SKILL_LV02",
            action_cond_id=197
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SP_RATE,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_SPB_LV02",
            action_cond_id=194
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
            action_cond_id=76
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.CRT_RATE,
            rate=0.03,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_CRT_LV03",
            action_cond_id=38
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SKILL_DAMAGE,
            rate=0.1,
            duration_time=10,
            duration_count=99,
            hit_attr_label="BOW_108_04_SKILL_LV03",
            action_cond_id=197
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF_SURROUNDING,
            parameter=BuffParameter.SP_RATE,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_SPB_LV03",
            action_cond_id=194
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
            action_cond_id=303020101
        )
    }
    on_1_plus_buffs = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.CRT_DAMAGE,
            rate=0.1,
            duration_time=10,
            duration_count=0,
            hit_attr_label="BOW_108_04_CRTDMG_LV03",
            action_cond_id=1176
        )
    }
    on_2_plus_buffs = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.SP_CHARGE_PCT_S1,
            rate=1,
            duration_time=0,
            duration_count=0,
            hit_attr_label="BOW_108_04_SP_LV03",
            action_cond_id=0
        )
    }

    expected_base_buffs = [expected_base_buffs_lv_1, expected_base_buffs_lv_2, expected_base_buffs_lv_3]

    # arr[i][j] is the additional buffs granted, i = skill level / j = count of teammates covered
    expected_additional_buffs = [
        [set(), set(), set(), set()],
        [set(), set(), set(), set()],
        [
            set(),
            on_0_plus_buffs,
            on_0_plus_buffs | on_1_plus_buffs,
            on_0_plus_buffs | on_1_plus_buffs | on_2_plus_buffs
        ]
    ]

    assert skill_data_base.max_level == 3

    for skill_lv in range(skill_data_base.max_level):
        for teammate_count, cond_enum in enumerate(SkillCondition.get_teammate_coverage_conditions()):
            skill_data = skill_data_base.with_conditions(SkillConditionComposite(cond_enum))

            expected_buffs = expected_base_buffs[skill_lv] | expected_additional_buffs[skill_lv][teammate_count]
            actual_buffs = skill_data.buffs[skill_lv]

            assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_has_phase(transformer_skill: SkillTransformer):
    # Summer Julietta S2
    # https://dragalialost.gamepedia.com/Summer_Julietta
    skill_data = transformer_skill.transform_supportive(104502012)

    # TEST: TBA - S!Julietta S2


def test_with_attack(transformer_skill: SkillTransformer):
    # Marth S2
    # https://dragalialost.gamepedia.com/Marth
    skill_data = transformer_skill.transform_supportive(101501022)

    # TEST: TBA - Marth S2


def test_with_attack_one_time_use(transformer_skill: SkillTransformer):
    # Lazry S1 @ High Power
    # https://dragalialost.gamepedia.com/Lazry
    skill_data = transformer_skill.transform_supportive(104502033)

    # TEST: TBA - Lazry S1
