import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer


def test_iter_entries_enhanced_s1(transformer_skill: SkillTransformer):
    # Summer Mitsuhide
    # https://dragalialost.wiki/w/Summer_Mitsuhide
    skill_data = transformer_skill.transform_attacking(103501033)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite(): 21.49,
        ConditionComposite([Condition.TARGET_SCORCHRENT, Condition.COMBO_GTE_0]): 21.49 * 1.10,
        ConditionComposite([Condition.TARGET_SCORCHRENT, Condition.COMBO_GTE_15]): 21.49 * 1.20,
        ConditionComposite([Condition.TARGET_SCORCHRENT, Condition.COMBO_GTE_30]): 21.49 * 1.30,
        ConditionComposite([Condition.TARGET_SCORCHRENT, Condition.COMBO_GTE_50]): 21.49 * 1.50,
    }

    expected = set(expected_addl_at_max.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        assert \
            entry.total_mod_at_max == pytest.approx(expected_addl_at_max[entry.condition_comp]), \
            entry.condition_comp
        del expected_addl_at_max[entry.condition_comp]

    assert len(expected_addl_at_max) == 0, f"Conditions not tested: {set(expected_addl_at_max.keys())}"


def test_enhanced_s1_scorchrent_combo_50(transformer_skill: SkillTransformer):
    # Summer Mitsuhide
    # https://dragalialost.wiki/w/Summer_Mitsuhide
    conditions = ConditionComposite([Condition.TARGET_SCORCHRENT, Condition.COMBO_GTE_50])

    transformer_skill.transform_attacking(103501033).with_conditions(conditions)
