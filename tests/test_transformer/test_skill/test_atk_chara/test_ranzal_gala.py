import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries_s1_no_ability(transformer_skill: SkillTransformer):
    # Gala Ranzal S1
    # https://dragalialost.wiki/w/Gala_Ranzal
    skill_data = transformer_skill.transform_attacking(101503011)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite(): 3.09 * 6
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


def test_iter_entries_s1_with_ability(transformer_skill: SkillTransformer):
    # Gala Ranzal S1
    # https://dragalialost.wiki/w/Gala_Ranzal
    skill_data = transformer_skill.transform_attacking(101503011, ability_ids=[124])

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite(Condition.SELF_GAUGE_FILLED_0): 3.09 * 6 * 1,
        ConditionComposite(Condition.SELF_GAUGE_FILLED_1): 3.09 * 6 * 1.2,
        ConditionComposite(Condition.SELF_GAUGE_FILLED_2): 3.09 * 6 * 2,
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


def test_s1_no_chara_ability(transformer_skill: SkillTransformer):
    # Gala Ranzal S1
    # https://dragalialost.wiki/w/Gala_Ranzal
    skill_data_base = transformer_skill.transform_attacking(101503011)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [6, 6, 6, 6]
    assert skill_data.hit_count_at_max == 6
    assert skill_data.total_mod == pytest.approx([
        2.464 * 6,
        2.728 * 6,
        3.036 * 6,
        3.09 * 6
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3.09 * 6)
    assert skill_data.mods == approx_matrix([
        [2.464] * 6,
        [2.728] * 6,
        [3.036] * 6,
        [3.09] * 6
    ])
    assert skill_data.mods_at_max == pytest.approx([3.09] * 6)
    assert skill_data.max_level == 4


def test_s1_has_chara_ability(transformer_skill: SkillTransformer):
    # Gala Ranzal S1
    # https://dragalialost.wiki/w/Gala_Ranzal
    skill_data_base = transformer_skill.transform_attacking(101503011, ability_ids=[124])

    dmg_up_rate = {
        ConditionComposite(Condition.SELF_GAUGE_FILLED_0): 1,
        ConditionComposite(Condition.SELF_GAUGE_FILLED_1): 1.2,
        ConditionComposite(Condition.SELF_GAUGE_FILLED_2): 2,
    }

    for cond_comp, up_rate in dmg_up_rate.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == [6, 6, 6, 6]
        assert skill_data.hit_count_at_max == 6
        assert skill_data.total_mod == pytest.approx([
            2.464 * 6 * up_rate,
            2.728 * 6 * up_rate,
            3.036 * 6 * up_rate,
            3.09 * 6 * up_rate
        ])
        assert skill_data.total_mod_at_max == pytest.approx(3.09 * up_rate * 6)
        assert skill_data.mods == approx_matrix([
            [2.464 * up_rate] * 6,
            [2.728 * up_rate] * 6,
            [3.036 * up_rate] * 6,
            [3.09 * up_rate] * 6
        ])
        assert skill_data.mods_at_max == pytest.approx([3.09 * up_rate] * 6)
        assert skill_data.max_level == 4
