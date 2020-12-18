import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries_s1_normal(transformer_skill: SkillTransformer):
    # Nadine S1
    # https://dragalialost.gamepedia.com/Nadine
    skill_data = transformer_skill.transform_attacking(105501021)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite(Condition.COVER_TEAMMATE_0): 13.152,
        ConditionComposite(Condition.COVER_TEAMMATE_1): 13.152 + 1.64,
        ConditionComposite(Condition.COVER_TEAMMATE_2): 13.152 + 3.29,
        ConditionComposite(Condition.COVER_TEAMMATE_3): 13.152 + 3.29
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


def test_iter_entries_s1_trendsetting(transformer_skill: SkillTransformer):
    # Nadine S1 @ Trendsetting
    # https://dragalialost.gamepedia.com/Nadine
    skill_data = transformer_skill.transform_attacking(105501023)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite(Condition.COVER_TEAMMATE_0): 4.384 * 3 + 3.29,
        ConditionComposite(Condition.COVER_TEAMMATE_1): 4.384 * 3 + 3.29,
        ConditionComposite(Condition.COVER_TEAMMATE_2): 4.384 * 3 + 5.75,
        ConditionComposite(Condition.COVER_TEAMMATE_3): 4.384 * 3 + 5.75
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


def test_s1_normal(transformer_skill: SkillTransformer):
    # Nadine S1 normal
    # https://dragalialost.gamepedia.com/Nadine
    skill_data_base = transformer_skill.transform_attacking(105501021)

    expected_mods = {
        ConditionComposite(Condition.COVER_TEAMMATE_0): [
            [11.936],
            [12.528],
            [13.152]
        ],
        ConditionComposite(Condition.COVER_TEAMMATE_1): [
            [11.936, 1.49],
            [12.528, 1.57],
            [13.152, 1.64]
        ],
        ConditionComposite(Condition.COVER_TEAMMATE_2): [
            [11.936, 2.98],
            [12.528, 3.13],
            [13.152, 3.29]
        ],
        ConditionComposite(Condition.COVER_TEAMMATE_3): [
            [11.936, 2.98],
            [12.528, 3.13],
            [13.152, 3.29]
        ]
    }
    expected_hits = {
        ConditionComposite(Condition.COVER_TEAMMATE_0): [2, 2, 2],
        ConditionComposite(Condition.COVER_TEAMMATE_1): [4, 4, 4],
        ConditionComposite(Condition.COVER_TEAMMATE_2): [5, 5, 5],
        ConditionComposite(Condition.COVER_TEAMMATE_3): [6, 6, 6]
    }

    for cond_comp, expected_mod in expected_mods.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == expected_hits[cond_comp]
        assert skill_data.hit_count_at_max == expected_hits[cond_comp][-1]
        assert skill_data.total_mod == pytest.approx([sum(mods) for mods in expected_mod])
        assert skill_data.total_mod_at_max == pytest.approx(sum(expected_mod[-1]))
        assert skill_data.mods == approx_matrix(expected_mod)
        assert skill_data.mods_at_max == pytest.approx(expected_mod[-1])
        assert skill_data.max_level == 3


def test_s1_trendsetting(transformer_skill: SkillTransformer):
    # Nadine S1 enhanced by S2
    # https://dragalialost.gamepedia.com/Nadine
    skill_data_base = transformer_skill.transform_attacking(105501023)

    expected_mods = {
        ConditionComposite(Condition.COVER_TEAMMATE_0): [
            [3.984, 3.984, 3.984, 2.98],
            [4.176, 4.176, 4.176, 3.13],
            [4.384, 4.384, 4.384, 3.29]
        ],
        ConditionComposite(Condition.COVER_TEAMMATE_1): [
            [3.984, 3.984, 3.984, 2.98],
            [4.176, 4.176, 4.176, 3.13],
            [4.384, 4.384, 4.384, 3.29]
        ],
        ConditionComposite(Condition.COVER_TEAMMATE_2): [
            [3.984, 3.984, 3.984, 5.22],
            [4.176, 4.176, 4.176, 5.48],
            [4.384, 4.384, 4.384, 5.75]
        ],
        ConditionComposite(Condition.COVER_TEAMMATE_3): [
            [3.984, 3.984, 3.984, 5.22],
            [4.176, 4.176, 4.176, 5.48],
            [4.384, 4.384, 4.384, 5.75]
        ]
    }
    expected_hits = {
        ConditionComposite(Condition.COVER_TEAMMATE_0): [5, 5, 5],
        ConditionComposite(Condition.COVER_TEAMMATE_1): [6, 6, 6],
        ConditionComposite(Condition.COVER_TEAMMATE_2): [7, 7, 7],
        ConditionComposite(Condition.COVER_TEAMMATE_3): [8, 8, 8]
    }

    for cond_comp, expected_mod in expected_mods.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == expected_hits[cond_comp]
        assert skill_data.hit_count_at_max == expected_hits[cond_comp][-1]
        assert skill_data.total_mod == pytest.approx([sum(mods) for mods in expected_mod])
        assert skill_data.total_mod_at_max == pytest.approx(sum(expected_mod[-1]))
        assert skill_data.mods == approx_matrix(expected_mod)
        assert skill_data.mods_at_max == pytest.approx(expected_mod[-1])
        assert skill_data.max_level == 3
