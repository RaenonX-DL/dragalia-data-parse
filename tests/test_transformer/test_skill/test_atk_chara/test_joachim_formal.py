from itertools import zip_longest

import pytest

from dlparse.enums import Condition, ConditionComposite, SkillCancelAction
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries_s1(transformer_skill: SkillTransformer):
    # Formal Joachim S1
    # https://dragalialost.gamepedia.com/Formal_Joachim
    skill_data = transformer_skill.transform_attacking(109503011)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite(): 10.12,
        ConditionComposite(Condition.CANCELS_FJOACHIM_S2): 20.64,
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
    # Formal Joachim S1
    # https://dragalialost.gamepedia.com/Formal_Joachim
    skill_data = transformer_skill.transform_attacking(109503011)

    expected_cancel_action_data = {(SkillCancelAction.ANY_ACTION, 1.3)}

    main_expected = [set(expected_cancel_action_data)] * 4
    main_actual = [
        {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
        for cancel_unit_lv in skill_data.cancel_unit_mtx
    ]

    main_symmetric_diff = [
        expected_lv.symmetric_difference(actual_lv)
        for expected_lv, actual_lv in zip_longest(main_expected, main_actual)
    ]

    assert not any(main_symmetric_diff), main_symmetric_diff


def test_cancel_s1_entries(transformer_skill: SkillTransformer):
    # Formal Joachim S1
    # https://dragalialost.gamepedia.com/Formal_Joachim
    skill_data = transformer_skill.transform_attacking(109503011)

    expected_cancel_action_data = {(SkillCancelAction.ANY_ACTION, 1.3)}

    for entry in skill_data.get_all_possible_entries():
        entry_expected = [set(expected_cancel_action_data)] * 4
        entry_actual = [
            {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
            for cancel_unit_lv in entry.cancel_unit_mtx
        ]

        entry_symmetric_diff = [
            expected_lv.symmetric_difference(actual_lv)
            for expected_lv, actual_lv in zip_longest(entry_expected, entry_actual)
        ]

        assert not any(entry_symmetric_diff), entry_symmetric_diff


def test_cancel_s2_data(transformer_skill: SkillTransformer):
    # Formal Joachim S2
    # https://dragalialost.gamepedia.com/Formal_Joachim
    skill_data = transformer_skill.transform_attacking(109503012)

    expected_cancel_action_data = {
        (SkillCancelAction.FORMAL_JOACHIM_S1, 1.5333333),
        (SkillCancelAction.ANY_ACTION, 2.16666675),
    }

    for entry in skill_data.get_all_possible_entries():
        entry_expected = [set(expected_cancel_action_data)] * 4
        entry_actual = [
            {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
            for cancel_unit_lv in entry.cancel_unit_mtx
        ]

        entry_symmetric_diff = [
            expected_lv.symmetric_difference(actual_lv)
            for expected_lv, actual_lv in zip_longest(entry_expected, entry_actual)
        ]

        assert not any(entry_symmetric_diff), entry_symmetric_diff


def test_cancel_s2_entries(transformer_skill: SkillTransformer):
    # Formal Joachim S2
    # https://dragalialost.gamepedia.com/Formal_Joachim
    skill_data = transformer_skill.transform_attacking(109503012)

    expected_cancel_action_data = {
        (SkillCancelAction.FORMAL_JOACHIM_S1, 1.5333333),
        (SkillCancelAction.ANY_ACTION, 2.16666675),
    }

    for entry in skill_data.get_all_possible_entries():
        entry_expected = [set(expected_cancel_action_data)] * 4
        entry_actual = [
            {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
            for cancel_unit_lv in entry.cancel_unit_mtx
        ]

        entry_symmetric_diff = [
            expected_lv.symmetric_difference(actual_lv)
            for expected_lv, actual_lv in zip_longest(entry_expected, entry_actual)
        ]

        assert not any(entry_symmetric_diff), entry_symmetric_diff


def test_s1(transformer_skill: SkillTransformer):
    # Formal Joachim S1
    # https://dragalialost.gamepedia.com/Formal_Joachim
    skill_data_base = transformer_skill.transform_attacking(109503011)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([8.19, 9.11, 10.12])
    assert skill_data.total_mod_at_max == pytest.approx(10.12)
    assert skill_data.mods == approx_matrix([[8.19], [9.11], [10.12]])
    assert skill_data.mods_at_max == pytest.approx([10.12])
    assert skill_data.max_level == 3


def test_s1_explode(transformer_skill: SkillTransformer):
    # Formal Joachim S1 @ Aced (S2-S1)
    # https://dragalialost.gamepedia.com/Formal_Joachim
    skill_data_base = transformer_skill.transform_attacking(109503011)

    # Cancels S2
    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.CANCELS_FJOACHIM_S2))

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([16.72, 18.58, 20.64])
    assert skill_data.total_mod_at_max == pytest.approx(20.64)
    assert skill_data.mods == approx_matrix([[16.72], [18.58], [20.64]])
    assert skill_data.mods_at_max == pytest.approx([20.64])
    assert skill_data.max_level == 3
