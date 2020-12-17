import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer


def test_iter_entries_s2(transformer_skill: SkillTransformer):
    # Delphi S2
    # https://dragalialost.gamepedia.com/Delphi
    skill_data = transformer_skill.transform_attacking(103505022)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        SkillConditionComposite(): 4.99,
        SkillConditionComposite(SkillCondition.TARGET_ELEM_LIGHT): 4.99,
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
