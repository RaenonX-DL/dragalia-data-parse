from dlparse.enums import BuffParameter, HitTargetSimple
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_partial_attacking(transformer_skill: SkillTransformer):
    # Elisanne S1
    # https://dragalialost.wiki/w/Elisanne
    skill_data_base = transformer_skill.transform_supportive(105402011)

    assert skill_data_base.max_level == 4

    expected_buffs_lv_1 = {
        BuffEffectInfo("BUF_ALL_ATK_SR_30_LV01", HitTargetSimple.TEAM, BuffParameter.ATK_BUFF, 0.1, 15, 0)
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BUF_ALL_ATK_SR_30_LV02", HitTargetSimple.TEAM, BuffParameter.ATK_BUFF, 0.15, 15, 0)
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("BUF_ALL_ATK_SR_30_LV03", HitTargetSimple.TEAM, BuffParameter.ATK_BUFF, 0.20, 15, 0)
    }
    expected_buffs_lv_4 = {
        BuffEffectInfo("BUF_ALL_ATK_SR_30_LV04", HitTargetSimple.TEAM, BuffParameter.ATK_BUFF, 0.25, 15, 0)
    }

    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3, expected_buffs_lv_4]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_4)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)
