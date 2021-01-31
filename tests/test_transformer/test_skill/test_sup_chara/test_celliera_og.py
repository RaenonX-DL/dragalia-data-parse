from dlparse.enums import BuffParameter, HitTargetSimple
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_s2(transformer_skill: SkillTransformer):
    # Original Celliera S2
    # https://dragalialost.wiki/w/Celliera
    skill_data_base = transformer_skill.transform_supportive(102402012)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        BuffEffectInfo("BUF_107_LV01", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.2, 10, 0),
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BUF_107_LV02", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.25, 10, 0),
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("BUF_107_LV03", HitTargetSimple.SELF, BuffParameter.ATK_BUFF, 0.25, 0, 0),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    # Base data
    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)
