from dlparse.enums import BuffParameter, Condition, ConditionComposite, HitTargetSimple
from dlparse.transformer import SkillTransformer
from tests.utils import BuffEffectInfo, check_buff_unit_match


def test_fs_dmg_up(transformer_skill: SkillTransformer):
    # MH Sarisse S2
    # https://dragalialost.wiki/w/Hunter_Sarisse
    skill_data_base = transformer_skill.transform_supportive(106502021)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        BuffEffectInfo("BOW_112_04_BA_LV01", HitTargetSimple.SELF, BuffParameter.FS_DAMAGE_BUFF, 0.6, 0, 1, 1)
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BOW_112_04_BA_LV02", HitTargetSimple.SELF, BuffParameter.FS_DAMAGE_BUFF, 0.8, 0, 1, 1)
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("BOW_112_04_BA_LV03", HitTargetSimple.SELF, BuffParameter.FS_DAMAGE_BUFF, 1, 0, 1, 1)
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3, check_stack_count=True)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs, check_stack_count=True)


def test_fs_spd(transformer_skill: SkillTransformer):
    # Linnea S2
    # https://dragalialost.wiki/w/Linnea
    skill_data_base = transformer_skill.transform_supportive(102505032)

    assert skill_data_base.max_level == 2

    expected_buffs_lv_1 = {
        BuffEffectInfo("BUF_205_BAC_LV01", HitTargetSimple.SELF, BuffParameter.FS_SPD, 0.2, 15, 0),
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BUF_205_BAC_LV02", HitTargetSimple.SELF, BuffParameter.FS_SPD, 0.3, 15, 0),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_2)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_shield_dmg(transformer_skill: SkillTransformer):
    # Yuya S2
    # https://dragalialost.wiki/w/Yuya
    skill_data_base = transformer_skill.transform_supportive(103401022)

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1 = {
        BuffEffectInfo("BUF_165_DEF_LV01", HitTargetSimple.TEAM, BuffParameter.DEF_BUFF, 0.1, 15, 0),
        BuffEffectInfo("BUF_165_SIELD_LV01", HitTargetSimple.TEAM, BuffParameter.SHIELD_SINGLE_DMG, 0.15, 0, 1),
        BuffEffectInfo("BUF_ALL_ATK_SR_30_LV01", HitTargetSimple.TEAM, BuffParameter.ATK_BUFF, 0.1, 15, 0),
    }
    expected_buffs_lv_2 = {
        BuffEffectInfo("BUF_165_DEF_LV02", HitTargetSimple.TEAM, BuffParameter.DEF_BUFF, 0.1, 15, 0),
        BuffEffectInfo("BUF_165_SIELD_LV02", HitTargetSimple.TEAM, BuffParameter.SHIELD_SINGLE_DMG, 0.2, 0, 1),
        BuffEffectInfo("BUF_ALL_ATK_SR_30_LV02", HitTargetSimple.TEAM, BuffParameter.ATK_BUFF, 0.15, 15, 0),
    }
    expected_buffs_lv_3 = {
        BuffEffectInfo("BUF_165_DEF_LV03", HitTargetSimple.TEAM, BuffParameter.DEF_BUFF, 0.1, 15, 0),
        BuffEffectInfo("BUF_165_SIELD_LV03", HitTargetSimple.TEAM, BuffParameter.SHIELD_SINGLE_DMG, 0.3, 0, 1),
        BuffEffectInfo("BUF_165_ATK_LV03", HitTargetSimple.TEAM, BuffParameter.ATK_BUFF, 0.15, 15, 0),
    }
    expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)


def test_shield_hp(transformer_skill: SkillTransformer):
    # Grace S1
    # https://dragalialost.wiki/w/Linnea
    skill_data_base = transformer_skill.transform_supportive(108505031)

    # SkillData.Ability - Ability.Condition & IDStr to Label

    assert skill_data_base.max_level == 3

    expected_buffs_lv_1_gte_40 = {
        BuffEffectInfo("BUF_189_BARRIER_LV03", HitTargetSimple.TEAM, BuffParameter.SHIELD_LIFE, 0.3, 0, 0),
        BuffEffectInfo("BUF_189_DMG_LV03", HitTargetSimple.SELF, BuffParameter.HP_FIX_BY_MAX, 0.3, 0, 0),
    }
    expected_buffs_lv_2_gte_40 = {
        BuffEffectInfo("BUF_189_BARRIER_LV03", HitTargetSimple.TEAM, BuffParameter.SHIELD_LIFE, 0.3, 0, 0),
        BuffEffectInfo("BUF_189_DMG_LV03", HitTargetSimple.SELF, BuffParameter.HP_FIX_BY_MAX, 0.3, 0, 0),
    }
    expected_buffs_lv_3_gte_40 = {
        BuffEffectInfo("BUF_189_BARRIER_LV03", HitTargetSimple.TEAM, BuffParameter.SHIELD_LIFE, 0.3, 0, 0),
        BuffEffectInfo("BUF_189_DMG_LV03", HitTargetSimple.SELF, BuffParameter.HP_FIX_BY_MAX, 0.3, 0, 0),
    }
    expected_buffs_lv_1_lt_40 = {
        BuffEffectInfo("BUF_ALL_DEF_SSR_30_LV01", HitTargetSimple.TEAM, BuffParameter.DEF_BUFF, 0.2, 15, 0),
    }
    expected_buffs_lv_2_lt_40 = {
        BuffEffectInfo("BUF_ALL_DEF_SSR_30_LV02", HitTargetSimple.TEAM, BuffParameter.DEF_BUFF, 0.25, 15, 0),
    }
    expected_buffs_lv_3_lt_40 = {
        BuffEffectInfo("BUF_ALL_DEF_SSR_30_LV03", HitTargetSimple.TEAM, BuffParameter.DEF_BUFF, 0.3, 15, 0),
    }
    expected_base_buffs_gte_40 = [expected_buffs_lv_1_gte_40, expected_buffs_lv_2_gte_40, expected_buffs_lv_3_gte_40]
    expected_base_buffs_lt_40 = [expected_buffs_lv_1_lt_40, expected_buffs_lv_2_lt_40, expected_buffs_lv_3_lt_40]

    # No conditions

    skill_data = skill_data_base.with_conditions()

    assert skill_data.max_lv_buffs == set()

    # HP >= 40%

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.SELF_HP_GTE_40))

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3_gte_40)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs_gte_40[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)

    # HP < 40%

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.SELF_HP_LT_40))

    check_buff_unit_match(skill_data.max_lv_buffs, expected_buffs_lv_3_lt_40)

    for skill_lv in range(skill_data_base.max_level):
        expected_buffs = expected_base_buffs_lt_40[skill_lv]
        actual_buffs = skill_data.buffs[skill_lv]

        check_buff_unit_match(actual_buffs, expected_buffs)
