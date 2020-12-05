from dlparse.enums import BuffParameter, HitTargetSimple, SkillCondition, SkillConditionComposite
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


def test_fs_spd(transformer_skill: SkillTransformer):
    # Linnea S2
    # https://dragalialost.gamepedia.com/Linnea
    skill_data_base = transformer_skill.transform_supportive(102505032)

    assert skill_data_base.max_level == 2

    expected_buffs_lv_1 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.FS_SPD,
            rate=0.2,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_205_BAC_LV01",
            action_cond_id=902,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_2 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.FS_SPD,
            rate=0.3,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_205_BAC_LV02",
            action_cond_id=903,
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


def test_shield_dmg(transformer_skill: SkillTransformer):
    # Yuya S2
    # https://dragalialost.gamepedia.com/Yuya
    skill_data_base = transformer_skill.transform_supportive(103401022)

    # Despite Yuya S2 only has 2 levels, no indicator can be used to limit the level discovery
    # while ATK effect can be discovered until level 4.
    # Therefore, the returned max level is 4 instead of 2.
    assert skill_data_base.max_level == 4

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
            parameter=BuffParameter.SHIELD_SINGLE_DMG,
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
            parameter=BuffParameter.SHIELD_SINGLE_DMG,
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
    expected_buffs_lv_3 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.ATK,
            rate=0.2,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_ATK_SR_30_LV03",
            action_cond_id=302030401,
            max_stack_count=0
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
            action_cond_id=302030501,
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


def test_shield_hp(transformer_skill: SkillTransformer):
    # Grace S1
    # https://dragalialost.gamepedia.com/Linnea
    skill_data_base = transformer_skill.transform_supportive(108505031)

    # SkillData.Ability - Ability.Condition & IDStr to Label

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1_gte_40 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.SHIELD_LIFE,
            rate=0.3,
            duration_time=0,
            duration_count=0,
            hit_attr_label="BUF_189_BARRIER_LV03",
            action_cond_id=504,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.HP_FIX_BY_MAX,
            rate=0.3,
            duration_time=0,
            duration_count=0,
            hit_attr_label="BUF_189_DMG_LV03",
            action_cond_id=0,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_2_gte_40 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.SHIELD_LIFE,
            rate=0.3,
            duration_time=0,
            duration_count=0,
            hit_attr_label="BUF_189_BARRIER_LV03",
            action_cond_id=504,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.HP_FIX_BY_MAX,
            rate=0.3,
            duration_time=0,
            duration_count=0,
            hit_attr_label="BUF_189_DMG_LV03",
            action_cond_id=0,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_3_gte_40 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.SHIELD_LIFE,
            rate=0.3,
            duration_time=0,
            duration_count=0,
            hit_attr_label="BUF_189_BARRIER_LV03",
            action_cond_id=504,
            max_stack_count=0
        ),
        SupportiveSkillUnit(
            target=HitTargetSimple.SELF,
            parameter=BuffParameter.HP_FIX_BY_MAX,
            rate=0.3,
            duration_time=0,
            duration_count=0,
            hit_attr_label="BUF_189_DMG_LV03",
            action_cond_id=0,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_1_lt_40 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.DEF,
            rate=0.2,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_DEF_SSR_30_LV01",
            action_cond_id=303030301,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_2_lt_40 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.DEF,
            rate=0.25,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_DEF_SSR_30_LV02",
            action_cond_id=303030401,
            max_stack_count=0
        ),
    }
    expected_buffs_lv_3_lt_40 = {
        SupportiveSkillUnit(
            target=HitTargetSimple.TEAM,
            parameter=BuffParameter.DEF,
            rate=0.3,
            duration_time=15,
            duration_count=0,
            hit_attr_label="BUF_ALL_DEF_SSR_30_LV03",
            action_cond_id=303030501,
            max_stack_count=0
        ),
    }
    expected_base_buffs_gte_40 = [expected_buffs_lv_1_gte_40, expected_buffs_lv_2_gte_40, expected_buffs_lv_3_gte_40]
    expected_base_buffs_lt_40 = [expected_buffs_lv_1_lt_40, expected_buffs_lv_2_lt_40, expected_buffs_lv_3_lt_40]

    # No conditions

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == set()

    # HP >= 40%

    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.SELF_HP_GTE_40))

    assert skill_data.max_lv_buffs == expected_buffs_lv_3_gte_40

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs_gte_40[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)

    # HP < 40%

    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.SELF_HP_LTE_40))

    assert skill_data.max_lv_buffs == expected_buffs_lv_3_lt_40

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs_lt_40[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)
