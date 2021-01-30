import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries_s2(transformer_skill: SkillTransformer):
    # Meene S2
    # https://dragalialost.wiki/w/Meene
    skill_data = transformer_skill.transform_attacking(106503032)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite([Condition.BULLETS_ON_MAP_0]): 1.67 * 0,
        ConditionComposite([Condition.BULLETS_ON_MAP_1]): 1.67 * 1,
        ConditionComposite([Condition.BULLETS_ON_MAP_2]): 1.67 * 2,
        ConditionComposite([Condition.BULLETS_ON_MAP_3]): 1.67 * 3,
        ConditionComposite([Condition.BULLETS_ON_MAP_4]): 1.67 * 4,
        ConditionComposite([Condition.BULLETS_ON_MAP_5]): 1.67 * 5,
        ConditionComposite([Condition.BULLETS_ON_MAP_6]): 1.67 * 6,
        ConditionComposite([Condition.BULLETS_ON_MAP_7]): 1.67 * 7,
        ConditionComposite([Condition.BULLETS_ON_MAP_8]): 1.67 * 8,
        ConditionComposite([Condition.BULLETS_ON_MAP_9]): 1.67 * 9,
    }

    expected = set(expected_addl_at_max.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        expected_total = 10 + expected_addl_at_max[entry.condition_comp]

        assert pytest.approx(expected_total) == entry.total_mod_at_max, entry.condition_comp
        del expected_addl_at_max[entry.condition_comp]

    assert len(expected_addl_at_max) == 0, f"Conditions not tested: {set(expected_addl_at_max.keys())}"


def test_s2(transformer_skill: SkillTransformer):
    # Meene S2
    # https://dragalialost.wiki/w/Meene
    skill_data_base = transformer_skill.transform_attacking(106503032)

    addl_hits = {
        ConditionComposite(Condition.BULLETS_ON_MAP_0): 0,
        ConditionComposite(Condition.BULLETS_ON_MAP_1): 1,
        ConditionComposite(Condition.BULLETS_ON_MAP_2): 2,
        ConditionComposite(Condition.BULLETS_ON_MAP_3): 3,
        ConditionComposite(Condition.BULLETS_ON_MAP_4): 4,
        ConditionComposite(Condition.BULLETS_ON_MAP_5): 5,
        ConditionComposite(Condition.BULLETS_ON_MAP_6): 6,
        ConditionComposite(Condition.BULLETS_ON_MAP_7): 7,
        ConditionComposite(Condition.BULLETS_ON_MAP_8): 8,
        ConditionComposite(Condition.BULLETS_ON_MAP_9): 9,
    }

    for cond_comp, bonus_hits in addl_hits.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == [1 + bonus_hits, 1 + bonus_hits]
        assert skill_data.hit_count_at_max == 1 + bonus_hits
        assert skill_data.total_mod == pytest.approx([
            9 + 1.5 * bonus_hits,
            10 + 1.67 * bonus_hits
        ])
        assert skill_data.total_mod_at_max == pytest.approx(10 + 1.67 * bonus_hits)
        assert skill_data.mods == approx_matrix([
            [9.0] + [1.5] * bonus_hits,
            [10.0] + [1.67] * bonus_hits
        ])
        assert skill_data.mods_at_max == pytest.approx([10.0] + [1.67] * bonus_hits)
        assert skill_data.max_level == 2


def test_s2_6_plus_butterflies(transformer_skill: SkillTransformer):
    # Meene S2 @ 6+ butterflies
    # https://dragalialost.wiki/w/Meene
    skill_data_base = transformer_skill.transform_attacking(106503036)

    addl_hits = {
        ConditionComposite(Condition.BULLETS_ON_MAP_0): 0,
        ConditionComposite(Condition.BULLETS_ON_MAP_1): 1,
        ConditionComposite(Condition.BULLETS_ON_MAP_2): 2,
        ConditionComposite(Condition.BULLETS_ON_MAP_3): 3,
        ConditionComposite(Condition.BULLETS_ON_MAP_4): 4,
        ConditionComposite(Condition.BULLETS_ON_MAP_5): 5,
        ConditionComposite(Condition.BULLETS_ON_MAP_6): 6,
        ConditionComposite(Condition.BULLETS_ON_MAP_7): 7,
        ConditionComposite(Condition.BULLETS_ON_MAP_8): 8,
        ConditionComposite(Condition.BULLETS_ON_MAP_9): 9,
    }

    for cond_comp, bonus_hits in addl_hits.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == [1 + bonus_hits, 1 + bonus_hits]
        assert skill_data.hit_count_at_max == 1 + bonus_hits
        assert skill_data.total_mod == pytest.approx([
            9 + 1.5 * bonus_hits,
            10 + 1.67 * bonus_hits
        ])
        assert skill_data.total_mod_at_max == pytest.approx(10 + 1.67 * bonus_hits)
        assert skill_data.mods == approx_matrix([
            [9.0] + [1.5] * bonus_hits,
            [10.0] + [1.67] * bonus_hits
        ])
        assert skill_data.mods_at_max == pytest.approx([10.0] + [1.67] * bonus_hits)
        assert skill_data.max_level == 2
