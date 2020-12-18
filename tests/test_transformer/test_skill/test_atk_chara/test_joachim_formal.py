import pytest

from dlparse.enums import Condition, ConditionComposite
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
