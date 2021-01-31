from dlparse.enums import BuffParameter, Condition, ConditionComposite, HitTargetSimple
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_s2(transformer_skill: SkillTransformer):
    # Lea S2
    # https://dragalialost.wiki/w/Lea
    skill_data_base = transformer_skill.transform_supportive(101501032)

    assert skill_data_base.max_level == 2

    expected_buffs_lv_1 = {
        BuffEffectInfo("BUF_221_DMG", HitTargetSimple.SELF, BuffParameter.HP_DECREASE_BY_MAX, 0.2, 0, 0),
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BUF_221_DMG", HitTargetSimple.SELF, BuffParameter.HP_DECREASE_BY_MAX, 0.2, 0, 0),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2]

    # Base data
    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.SELF_HP_GTE_60))

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_2)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)
