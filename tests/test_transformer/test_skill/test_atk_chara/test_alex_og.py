import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer


def test_iter_entries_s2(transformer_skill: SkillTransformer):
    # Original Alex S2
    # https://dragalialost.wiki/w/Alex
    skill_data = transformer_skill.transform_attacking(103405022)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite(): 2.01 * 3 + 4.02,
        ConditionComposite(Condition.TARGET_BK_STATE): 2.01 * 3 + 4.02,
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


def test_og_alex_s2(transformer_skill: SkillTransformer):
    # Original Alex S2
    # https://dragalialost.wiki/w/Alex
    skill_data_base = transformer_skill.transform_attacking(103405022)

    # Not BK
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        1.64 * 3 + 3.27,
        1.82 * 3 + 3.62,
        2.01 * 3 + 4.02
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.01 * 3 + 4.02)
    assert skill_data.mods == [
        [1.64] * 2 + [3.27] + [1.64],
        [1.82] * 2 + [3.62] + [1.82],
        [2.01] * 2 + [4.02] + [2.01]
    ]
    assert skill_data.mods_at_max == [2.01] * 2 + [4.02] + [2.01]
    assert skill_data.max_level == 3

    # In BK
    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.TARGET_BK_STATE))

    assert skill_data.hit_count == [4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        3.28 * 3 + 6.54,
        3.64 * 3 + 7.24,
        2.01 * 3 + 4.02
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.01 * 3 + 4.02)
    assert skill_data.mods == [
        [3.28] * 2 + [6.54] + [3.28],
        [3.64] * 2 + [7.24] + [3.64],
        [2.01] * 2 + [4.02] + [2.01]
    ]
    assert skill_data.mods_at_max == [2.01] * 2 + [4.02] + [2.01]
    assert skill_data.max_level == 3
