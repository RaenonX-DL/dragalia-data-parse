from dlparse.enums import BuffParameter, HitTargetSimple
from dlparse.model import SupportiveSkillUnit
from dlparse.transformer import SkillTransformer


def test_fs_dmg_up(transformer_skill: SkillTransformer):
    # MH Sarisse
    # https://dragalialost.gamepedia.com/Hunter_Sarisse
    skill_data_base = transformer_skill.transform_supportive(106502021)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.FS_DAMAGE,
            rate=0.6,
            duration_time=0,
            duration_count=1,
            hit_attr_label="BOW_112_04_BA_LV01",
            action_cond_id=432,
            max_stack_count=1
        ),
    }
    expected_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.FS_DAMAGE,
            rate=0.8,
            duration_time=0,
            duration_count=1,
            hit_attr_label="BOW_112_04_BA_LV02",
            action_cond_id=456,
            max_stack_count=1
        ),
    }
    expected_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.FS_DAMAGE,
            rate=1,
            duration_time=0,
            duration_count=1,
            hit_attr_label="BOW_112_04_BA_LV03",
            action_cond_id=457,
            max_stack_count=1
        ),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_buffs_lv_3

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)


def test_shield_hp(transformer_skill: SkillTransformer):
    # Yuya
    # https://dragalialost.gamepedia.com/Yuya
    skill_data_base = transformer_skill.transform_supportive(103401022)

    assert skill_data_base.max_level == 2

    expected_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.DEF,
            rate=0.1,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_165_DEF_LV01",
            action_cond_id=303030101,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.SHIELD_DMG,
            rate=0.15,
            duration_time=0,
            duration_count=1,
            hit_attr_label="BUF_165_SIELD_LV01",
            action_cond_id=316010301,
            max_stack_count=1
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.1,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_ATK_SR_30_LV01",
            action_cond_id=302030201,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.DEF,
            rate=0.1,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_165_DEF_LV02",
            action_cond_id=303030101,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.SHIELD_DMG,
            rate=0.2,
            duration_time=0,
            duration_count=1,
            hit_attr_label="BUF_165_SIELD_LV02",
            action_cond_id=316010401,
            max_stack_count=1
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.15,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_ATK_SR_30_LV02",
            action_cond_id=302030301,
            max_stack_count=0
        ),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2]

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == expected_buffs_lv_2

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)
