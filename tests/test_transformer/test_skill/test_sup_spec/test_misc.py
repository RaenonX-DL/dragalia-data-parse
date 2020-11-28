from dlparse.enums import BuffParameter, HitTargetSimple
from dlparse.model import SupportiveSkillUnit
from dlparse.transformer import SkillTransformer


def test_partial_attacking(transformer_skill: SkillTransformer):
    # Elisanne S1
    # https://dragalialost.gamepedia.com/Elisanne
    skill_data_base = transformer_skill.transform_supportive(105402011)

    assert skill_data_base.max_level == 4

    expected_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.10,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_ATK_SR_30_LV01",
            action_cond_id=302030201
        ),
    }
    expected_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_ATK_SR_30_LV02",
            action_cond_id=302030301
        ),
    }
    expected_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.20,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_ATK_SR_30_LV03",
            action_cond_id=302030401
        ),
    }
    expected_buffs_lv_4 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.25,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_ATK_SR_30_LV04",
            action_cond_id=302030501
        ),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3, expected_buffs_lv_4]

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_buffs_lv_4
    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)
