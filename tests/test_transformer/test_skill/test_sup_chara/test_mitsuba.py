from dlparse.enums import BuffParameter, HitTargetSimple
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_s2_tempura(transformer_skill: SkillTransformer):
    # Mitsuba S2 in Tempura
    # https://dragalialost.wiki/w/Mitsuba
    skill_data_base = transformer_skill.transform_supportive(103502024)

    assert skill_data_base.max_level == 2

    expected_buffs_lv_1 = {
        BuffEffectInfo("DAG_119_04_2_BUF_LV01", HitTargetSimple.TEAM, BuffParameter.CRT_DAMAGE_BUFF, 0.5, 15, 0),
        BuffEffectInfo("DAG_119_04_2_INSP_LV01", HitTargetSimple.TEAM, BuffParameter.INSPIRE_LEVEL, 2, 0, 1)
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("DAG_119_04_2_BUF_LV02", HitTargetSimple.TEAM, BuffParameter.CRT_DAMAGE_BUFF, 0.5, 15, 0),
        BuffEffectInfo("DAG_119_04_2_INSP_LV02", HitTargetSimple.TEAM, BuffParameter.INSPIRE_LEVEL, 3, 0, 1)
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2]

    # Base data
    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_2)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)
