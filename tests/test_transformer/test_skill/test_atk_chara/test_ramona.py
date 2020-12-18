import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries_s1(transformer_skill: SkillTransformer):
    # Ramona S1
    # https://dragalialost.gamepedia.com/Ramona
    skill_data = transformer_skill.transform_attacking(104501011)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite([Condition.ADDL_INPUT_0]): 3.76 + 2.93 * 3 + 2.93 * 0,
        ConditionComposite([Condition.ADDL_INPUT_1]): 3.76 + 2.93 * 3 + 2.93 * 1,
        ConditionComposite([Condition.ADDL_INPUT_2]): 3.76 + 2.93 * 3 + 2.93 * 2,
        ConditionComposite([Condition.ADDL_INPUT_3]): 3.76 + 2.93 * 3 + 2.93 * 3,
        ConditionComposite([Condition.ADDL_INPUT_4]): 3.76 + 2.93 * 3 + 2.93 * 4,
        ConditionComposite([Condition.ADDL_INPUT_5]): 3.76 + 2.93 * 3 + 2.93 * 5,
        ConditionComposite([Condition.ADDL_INPUT_6]): 3.76 + 2.93 * 3 + 2.93 * 6,
        ConditionComposite([Condition.ADDL_INPUT_0, Condition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 0,
        ConditionComposite([Condition.ADDL_INPUT_1, Condition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 1,
        ConditionComposite([Condition.ADDL_INPUT_2, Condition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 2,
        ConditionComposite([Condition.ADDL_INPUT_3, Condition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 3,
        ConditionComposite([Condition.ADDL_INPUT_4, Condition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 4,
        ConditionComposite([Condition.ADDL_INPUT_5, Condition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 5,
        ConditionComposite([Condition.ADDL_INPUT_6, Condition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 6,
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
    # Ramona S1
    # https://dragalialost.gamepedia.com/Ramona
    skill_data_base = transformer_skill.transform_attacking(104501011)

    pre_dmg = [
        [3.05] + [2.37] * 3,
        [3.39] + [2.63] * 3,
        [3.76] + [2.93] * 3
    ]
    addl_hits = {
        ConditionComposite(Condition.ADDL_INPUT_0): 0,
        ConditionComposite(Condition.ADDL_INPUT_1): 1,
        ConditionComposite(Condition.ADDL_INPUT_2): 2,
        ConditionComposite(Condition.ADDL_INPUT_3): 3,
        ConditionComposite(Condition.ADDL_INPUT_4): 4,
        ConditionComposite(Condition.ADDL_INPUT_5): 5,
        ConditionComposite(Condition.ADDL_INPUT_6): 6,
    }
    post_dmg = [
        [],
        [],
        []
    ]

    for cond_comp, bonus_hits in addl_hits.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == [4 + bonus_hits, 4 + bonus_hits, 4 + bonus_hits]
        assert skill_data.hit_count_at_max == 4 + bonus_hits
        assert skill_data.total_mod == pytest.approx([
            sum(pre_dmg[0]) + 2.37 * bonus_hits + sum(post_dmg[0]),
            sum(pre_dmg[1]) + 2.63 * bonus_hits + sum(post_dmg[1]),
            sum(pre_dmg[2]) + 2.93 * bonus_hits + sum(post_dmg[2]),
        ])
        assert skill_data.total_mod_at_max == pytest.approx(sum(pre_dmg[2]) + 2.93 * bonus_hits + sum(post_dmg[2]))
        assert skill_data.mods == approx_matrix([
            pre_dmg[0] + [2.37] * bonus_hits + post_dmg[0],
            pre_dmg[1] + [2.63] * bonus_hits + post_dmg[1],
            pre_dmg[2] + [2.93] * bonus_hits + post_dmg[2],
        ])
        assert skill_data.mods_at_max == pytest.approx(pre_dmg[2] + [2.93] * bonus_hits + post_dmg[2])
        assert skill_data.max_level == 3
