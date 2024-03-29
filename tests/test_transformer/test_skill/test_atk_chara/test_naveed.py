import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer


def test_naveed_s1(transformer_skill: SkillTransformer):
    # Naveed
    # https://dragalialost.wiki/w/Naveed
    skill_data = transformer_skill.transform_attacking(101501011)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite(Condition.BULLETS_SUMMONED_0): 3.47 * 4 + 1.4 * 3 * 0,
        ConditionComposite(Condition.BULLETS_SUMMONED_1): 3.47 * 4 + 1.4 * 3 * 1,
        ConditionComposite(Condition.BULLETS_SUMMONED_2): 3.47 * 4 + 1.4 * 3 * 2,
        ConditionComposite(Condition.BULLETS_SUMMONED_3): 3.47 * 4 + 1.4 * 3 * 3,
        ConditionComposite(Condition.BULLETS_SUMMONED_4): 3.47 * 4 + 1.4 * 3 * 4,
        ConditionComposite(Condition.BULLETS_SUMMONED_5): 3.47 * 4 + 1.4 * 3 * 5,
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
