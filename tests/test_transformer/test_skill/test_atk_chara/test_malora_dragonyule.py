import pytest

from dlparse.enums import Condition, ConditionComposite, SkillCancelAction
from dlparse.transformer import SkillTransformer
from tests.utils import CancelUnitInfo, approx_matrix, check_cancel_unit_match


def test_iter_entries_s1(transformer_skill: SkillTransformer):
    # Dragonyule Malora S1
    # https://dragalialost.wiki/w/Dragonyule_Malora
    skill_data = transformer_skill.transform_attacking(104504021)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite(): 4.67 * 2,
        ConditionComposite(Condition.TARGET_SHADOW): 4.67 * 2,
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


def test_s1_cancel_data(transformer_skill: SkillTransformer):
    # Dragonyule Malora S1
    # https://dragalialost.wiki/w/Dragonyule_Malora
    skill_data = transformer_skill.transform_attacking(104504021)

    for entry in skill_data.get_all_possible_entries():
        main_expected = [CancelUnitInfo(action=SkillCancelAction.MOTION_ENDS, time=2.266667)]

        for actual_cancel_units_lv in entry.cancel_unit_mtx:
            check_cancel_unit_match(actual_cancel_units_lv, main_expected)


def test_s2(transformer_skill: SkillTransformer):
    # Dragonyule Malora S2
    # https://dragalialost.wiki/w/Dragonyule_Malora
    skill_data_base = transformer_skill.transform_attacking(104504022)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([3.86 * 3, 4.32 * 3])
    assert skill_data.total_mod_at_max == pytest.approx(4.32 * 3)
    assert skill_data.mods == approx_matrix([[3.86] * 3, [4.32] * 3])
    assert skill_data.mods_at_max == pytest.approx([4.32] * 3)
    assert skill_data.max_level == 2

    # Target DEF down
    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.TARGET_DEF_DOWN))

    assert skill_data.hit_count == [3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([6.948 * 3, 7.776 * 3])
    assert skill_data.total_mod_at_max == pytest.approx(7.776 * 3)
    assert skill_data.mods == approx_matrix([[6.948] * 3, [7.776] * 3])
    assert skill_data.mods_at_max == pytest.approx([7.776] * 3)
    assert skill_data.max_level == 2
