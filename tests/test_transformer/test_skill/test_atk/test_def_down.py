from dlparse.enums import BuffParameter, SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import DebuffInfo, check_debuff_unit_match


def test_unstackable_1(transformer_skill: SkillTransformer):
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


def test_unstackable_2(transformer_skill: SkillTransformer):
    # Raemond S1
    # https://dragalialost.gamepedia.com/Raemond
    skill_data = transformer_skill.transform_attacking(101304011).with_conditions()

    expected_debuffs_lv_1 = [DebuffInfo("SWD_001_02_H02_DEF_RAIMUND_LV01", BuffParameter.DEF, -0.05, 100, 10, False)]
    expected_debuffs_lv_2 = [DebuffInfo("SWD_001_02_H02_DEF_RAIMUND_LV02", BuffParameter.DEF, -0.05, 100, 10, False)]
    expected_debuffs_lv_3 = [DebuffInfo("SWD_001_02_H02_DEF_RAIMUND_LV03", BuffParameter.DEF, -0.05, 100, 10, False)]

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


def test_elemental_restricted(transformer_skill: SkillTransformer):
    # Dragonyule Malora S1
    # https://dragalialost.gamepedia.com/Dragonyule_Malora
    skill_data_base = transformer_skill.transform_attacking(104504021)

    # Base data
    skill_data = skill_data_base.with_conditions()

    expected_debuffs_lv_1 = []
    expected_debuffs_lv_2 = []
    expected_debuffs_lv_3 = []

    expected_debuffs = [expected_debuffs_lv_1, expected_debuffs_lv_2, expected_debuffs_lv_3]

    assert skill_data.max_level == 3

    for skill_lv in range(skill_data.max_level):
        expected_buffs = expected_debuffs[skill_lv]
        actual_buffs = skill_data.debuffs[skill_lv]

        check_debuff_unit_match(actual_buffs, expected_buffs)

    # Flame-attuned (should be ineffective)
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_ELEM_FLAME))

    expected_debuffs_lv_1 = []
    expected_debuffs_lv_2 = []
    expected_debuffs_lv_3 = []

    expected_debuffs = [expected_debuffs_lv_1, expected_debuffs_lv_2, expected_debuffs_lv_3]

    assert skill_data.max_level == 3

    for skill_lv in range(skill_data.max_level):
        expected_buffs = expected_debuffs[skill_lv]
        actual_buffs = skill_data.debuffs[skill_lv]

        check_debuff_unit_match(actual_buffs, expected_buffs)

    # Shadow-attuned (should be effective)
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_ELEM_SHADOW))

    expected_debuffs_lv_1 = [
        DebuffInfo("AXE_113_04_H01_LV01", BuffParameter.DEF, -0.15, 100, 15, False),
        DebuffInfo("AXE_113_04_H02_LV01", BuffParameter.DEF, -0.15, 100, 15, False)
    ]
    expected_debuffs_lv_2 = [
        DebuffInfo("AXE_113_04_H01_LV02", BuffParameter.DEF, -0.15, 100, 15, False),
        DebuffInfo("AXE_113_04_H02_LV02", BuffParameter.DEF, -0.15, 100, 15, False)
    ]
    expected_debuffs_lv_3 = [
        DebuffInfo("AXE_113_04_H01_LV03", BuffParameter.DEF, -0.15, 100, 15, False),
        DebuffInfo("AXE_113_04_H02_LV03", BuffParameter.DEF, -0.15, 100, 15, False)
    ]

    expected_debuffs = [expected_debuffs_lv_1, expected_debuffs_lv_2, expected_debuffs_lv_3]

    assert skill_data.max_level == 3

    for skill_lv in range(skill_data.max_level):
        expected_buffs = expected_debuffs[skill_lv]
        actual_buffs = skill_data.debuffs[skill_lv]

        check_debuff_unit_match(actual_buffs, expected_buffs)


def test_area(transformer_skill: SkillTransformer):
    # Wedding Elisanne S2
    # https://dragalialost.gamepedia.com/Wedding_Elisanne
    skill_data = transformer_skill.transform_attacking(101503022).with_conditions()

    expected_debuffs_lv_1 = [DebuffInfo("SWD_111_04_DEF_DOWN_FLD_LV01", BuffParameter.DEF, -0.15, 0, 10, True)]
    expected_debuffs_lv_2 = [DebuffInfo("SWD_111_04_DEF_DOWN_FLD_LV02", BuffParameter.DEF, -0.15, 0, 10, True)]

    expected_debuffs = [expected_debuffs_lv_1, expected_debuffs_lv_2]

    assert skill_data.max_level == 2

    for skill_lv in range(skill_data.max_level):
        expected_buffs = expected_debuffs[skill_lv]
        actual_buffs = skill_data.debuffs[skill_lv]

        check_debuff_unit_match(actual_buffs, expected_buffs)
