from dlparse.enums import BuffParameter, HitTargetSimple
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_s2(transformer_skill: SkillTransformer):
    # Lucretia S2
    # https://dragalialost.wiki/w/Lucretia
    skill_data_base = transformer_skill.transform_supportive(107504012)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        BuffEffectInfo("BUF_119_ATACK_LV01", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.1, 10, 0),
        BuffEffectInfo("BUF_119_TENSION_LV01", HitTargetSimple.SELF, BuffParameter.ENERGY_LEVEL, 1, 0, 1)
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BUF_119_ATACK_LV02", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.1, 10, 0),
        BuffEffectInfo("BUF_119_TENSION_LV02", HitTargetSimple.SELF, BuffParameter.ENERGY_LEVEL, 2, 0, 1)
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("BUF_119_ATACK_LV03", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.15, 15, 0),
        BuffEffectInfo("BUF_119_TENSION_LV03", HitTargetSimple.SELF, BuffParameter.ENERGY_LEVEL, 3, 0, 1)
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    # Base data
    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)
