from dlparse.enums import BuffParameter
from dlparse.transformer import SkillTransformer
from tests.utils import DebuffInfo, check_debuff_unit_match


def test_unstackable(transformer_skill: SkillTransformer):
    # Original Alex S1
    # https://dragalialost.gamepedia.com/Alex
    skill_data = transformer_skill.transform_attacking(103405021).with_conditions()

    expected_debuffs_lv_1 = []
    expected_debuffs_lv_2 = (
            [DebuffInfo("DAG_117_03_H01_180_SHANON_LV02", BuffParameter.DEF, -0.05, 100, 10, False)] * 3
            + [DebuffInfo("DAG_117_03_H02_180_SHANON_LV02", BuffParameter.DEF, -0.05, 100, 10, False)] * 1
    )
    expected_debuffs_lv_3 = (
            [DebuffInfo("DAG_117_03_H01_180_SHANON_LV03", BuffParameter.DEF, -0.05, 100, 10, False)] * 3
            + [DebuffInfo("DAG_117_03_H02_180_SHANON_LV03", BuffParameter.DEF, -0.05, 100, 10, False)] * 1
    )

    expected_debuffs = [expected_debuffs_lv_1, expected_debuffs_lv_2, expected_debuffs_lv_3]

    assert skill_data.max_level == 3

    for skill_lv in range(skill_data.max_level):
        expected_buffs = expected_debuffs[skill_lv]
        actual_buffs = skill_data.debuffs[skill_lv]

        check_debuff_unit_match(actual_buffs, expected_buffs)


def test_stackable(transformer_skill: SkillTransformer):
    # Curran S1
    # https://dragalialost.gamepedia.com/Curran
    skill_data = transformer_skill.transform_attacking(104505011).with_conditions()

    expected_debuffs_lv_1 = []
    expected_debuffs_lv_2 = ([DebuffInfo("AXE_105_04_H01_LV02", BuffParameter.DEF, -0.05, 50, 10, True)] * 3
                             + [DebuffInfo("AXE_105_04_H02_LV02", BuffParameter.DEF, -0.05, 50, 10, True)] * 1)
    expected_debuffs_lv_3 = ([DebuffInfo("AXE_105_04_H01_LV03", BuffParameter.DEF, -0.05, 50, 10, True)] * 3
                             + [DebuffInfo("AXE_105_04_H02_LV03", BuffParameter.DEF, -0.05, 50, 10, True)] * 1)
    expected_debuffs_lv_4 = ([DebuffInfo("AXE_105_04_H01_LV04", BuffParameter.DEF, -0.05, 100, 10, True)] * 3
                             + [DebuffInfo("AXE_105_04_H02_LV04", BuffParameter.DEF, -0.05, 100, 10, True)] * 1)

    expected_debuffs = [expected_debuffs_lv_1, expected_debuffs_lv_2, expected_debuffs_lv_3, expected_debuffs_lv_4]

    assert skill_data.max_level == 4

    for skill_lv in range(skill_data.max_level):
        expected_buffs = expected_debuffs[skill_lv]
        actual_buffs = skill_data.debuffs[skill_lv]

        check_debuff_unit_match(actual_buffs, expected_buffs)
