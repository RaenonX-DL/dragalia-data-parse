import pytest

from dlparse.enums import BuffParameter, SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import DebuffInfo, approx_matrix, check_debuff_unit_match


def test_iter_entries_s1(transformer_skill: SkillTransformer):
    # Nobunaga
    # https://dragalialost.gamepedia.com/Nobunaga
    skill_data = transformer_skill.transform_attacking(102501031)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        SkillConditionComposite(): 7.13,
        SkillConditionComposite(SkillCondition.MARK_EXPLODES): 15.65,
    }

    expected = set(expected_addl_at_max.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        assert \
            pytest.approx(expected_addl_at_max[entry.condition_comp]) == entry.total_mod_at_max, \
            entry.condition_comp
        del expected_addl_at_max[entry.condition_comp]

    assert len(expected_addl_at_max) == 0, f"Conditions not tested: {set(expected_addl_at_max.keys())}"


def test_s1(transformer_skill: SkillTransformer):
    # Nobunaga
    # https://dragalialost.gamepedia.com/Nobunaga
    skill_data_base = transformer_skill.transform_attacking(102501031)

    # Skill
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([6.47, 6.8, 7.13])
    assert skill_data.total_mod_at_max == pytest.approx(7.13)
    assert skill_data.mods == approx_matrix([[6.47], [6.8], [7.13]])
    assert skill_data.mods_at_max == pytest.approx([7.13])
    assert skill_data.max_level == 3

    # Mark exploded
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.MARK_EXPLODES))

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([14.2, 14.9, 15.65])
    assert skill_data.total_mod_at_max == pytest.approx(15.65)
    assert skill_data.mods == approx_matrix([[14.2], [14.9], [15.65]])
    assert skill_data.mods_at_max == pytest.approx([15.65])
    assert skill_data.max_level == 3


def test_s1_mark(transformer_skill: SkillTransformer):
    # Nobunaga
    # https://dragalialost.gamepedia.com/Nobunaga
    skill_data_base = transformer_skill.transform_attacking(102501031)

    assert skill_data_base.max_level == 3

    expected_debuffs_lv_1 = [
        DebuffInfo("KAT_112_04_ADDDAMAGE_LV01", BuffParameter.MARK, 0, 100, 30, False),
    ]
    expected_debuffs_lv_2 = [
        DebuffInfo("KAT_112_04_ADDDAMAGE_LV02", BuffParameter.MARK, 0, 100, 30, False),
    ]
    expected_debuffs_lv_3 = [
        DebuffInfo("KAT_112_04_ADDDAMAGE_LV03", BuffParameter.MARK, 0, 100, 30, False),
    ]

    expected_base_debuffs = [expected_debuffs_lv_1, expected_debuffs_lv_2, expected_debuffs_lv_3]

    skill_data = skill_data_base.with_conditions()

    for skill_lv in range(skill_data_base.max_level):
        expected_debuffs = expected_base_debuffs[skill_lv]
        actual_debuffs = skill_data.debuffs[skill_lv]

        check_debuff_unit_match(actual_debuffs, expected_debuffs)
