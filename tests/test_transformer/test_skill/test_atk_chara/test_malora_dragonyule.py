from itertools import zip_longest

import pytest

from dlparse.enums import Condition, ConditionComposite, SkillCancelAction
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


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


def test_cancel_s1_data(transformer_skill: SkillTransformer):
    # Dragonyule Malora S1
    # https://dragalialost.wiki/w/Dragonyule_Malora
    skill_data = transformer_skill.transform_attacking(104504021)

    expected_cancel_action_data = {(SkillCancelAction.MOTION_ENDS, 2.266667)}

    main_expected = [set(expected_cancel_action_data)] * 4
    main_actual = [
        {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
        for cancel_unit_lv in skill_data.cancel_unit_mtx
    ]

    for expected_lv, actual_lv in zip_longest(main_expected, main_actual):
        diff = expected_lv.symmetric_difference(actual_lv)
        assert len(diff) == 0, diff


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
