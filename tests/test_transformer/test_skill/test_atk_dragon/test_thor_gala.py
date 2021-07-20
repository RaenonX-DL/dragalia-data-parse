import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries_s1(transformer_skill: SkillTransformer):
    # Lathna S1
    # https://dragalialost.wiki/w/Lathna
    skill_data = transformer_skill.transform_attacking(200504121)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite([Condition.ADDL_INPUT_0]): 3.25,
        ConditionComposite([Condition.ADDL_INPUT_1]): 3.25,
        ConditionComposite([Condition.ADDL_INPUT_2]): 3.25,
        ConditionComposite([Condition.ADDL_INPUT_3]): 7.85,
        ConditionComposite([Condition.ADDL_INPUT_4]): 7.85,
        ConditionComposite([Condition.ADDL_INPUT_5]): 7.85,
        ConditionComposite([Condition.ADDL_INPUT_6]): 13.8,
        ConditionComposite([Condition.ADDL_INPUT_7]): 13.8,
        ConditionComposite([Condition.ADDL_INPUT_8]): 13.8,
        ConditionComposite([Condition.ADDL_INPUT_9]): 17.8,
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


def test_ult_tap_9(transformer_skill: SkillTransformer):
    # Gala Thor Ult
    # https://dragalialost.wiki/w/Gala_Thor
    skill_data_base = transformer_skill.transform_attacking(200504121)

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.ADDL_INPUT_9))

    assert skill_data.hit_count == [1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([
        11.05,
        17.80,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(17.80)
    assert skill_data.mods == approx_matrix([
        [11.05],
        [17.80],
    ])
    assert skill_data.mods_at_max == pytest.approx([17.80])
    assert skill_data.max_level == 2
