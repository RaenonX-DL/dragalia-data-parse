from itertools import product

import pytest

from dlparse.enums import Condition, ConditionCategories, ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries_s2(transformer_skill: SkillTransformer):
    # Lapis S2
    # https://dragalialost.wiki/w/Lapis

    skill_data = transformer_skill.transform_attacking(109502012, is_exporting=True)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_conds = [
        Condition.SELF_LAPIS_CARD_0,
        Condition.SELF_LAPIS_CARD_1,
        Condition.SELF_LAPIS_CARD_2,
        Condition.SELF_LAPIS_CARD_3,
    ]
    expected_conds_up_rate = {
        ConditionComposite(addl_cond): min(ConditionCategories.self_lapis_card.convert(addl_cond) * 0.2, 0.8)
        for addl_cond in expected_addl_conds
    }

    expected = set(expected_conds_up_rate.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        expected_rate = 15.05 * 2 * (1 + expected_conds_up_rate[entry.condition_comp])

        assert entry.total_mod_at_max == pytest.approx(expected_rate), entry.condition_comp
        del expected_conds_up_rate[entry.condition_comp]

    assert len(expected_conds_up_rate) == 0, f"Conditions not tested: {list(sorted(expected_conds_up_rate.keys()))}"

    # Not exporting
    skill_data = transformer_skill.transform_attacking(109502012, is_exporting=False)

    possible_entries = skill_data.get_all_possible_entries()

    expected_buff_count_conds = [
        Condition.SELF_BUFF_0,
        Condition.SELF_BUFF_1,
        Condition.SELF_BUFF_2,
        Condition.SELF_BUFF_3,
        Condition.SELF_BUFF_4,
        Condition.SELF_BUFF_5,
        Condition.SELF_BUFF_6,
        Condition.SELF_BUFF_7,
        Condition.SELF_BUFF_8,
        Condition.SELF_BUFF_9,
        Condition.SELF_BUFF_10,
        Condition.SELF_BUFF_15,
        Condition.SELF_BUFF_20,
        Condition.SELF_BUFF_25,
        Condition.SELF_BUFF_30,
        Condition.SELF_BUFF_35,
        Condition.SELF_BUFF_40,
        Condition.SELF_BUFF_45,
        Condition.SELF_BUFF_50,
    ]
    expected_addl_conds = [
        Condition.SELF_LAPIS_CARD_0,
        Condition.SELF_LAPIS_CARD_1,
        Condition.SELF_LAPIS_CARD_2,
        Condition.SELF_LAPIS_CARD_3,
    ]
    expected_conds_up_rate = {
        ConditionComposite([buff_count_cond, addl_cond]):
            min(
                ConditionCategories.self_buff_count.convert(buff_count_cond) * 0.05
                + ConditionCategories.self_lapis_card.convert(addl_cond) * 0.2,
                0.8
            )
        for buff_count_cond, addl_cond in product(expected_buff_count_conds, expected_addl_conds)
    }

    expected = set(expected_conds_up_rate.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        expected_rate = 15.05 * 2 * (1 + expected_conds_up_rate[entry.condition_comp])

        assert entry.total_mod_at_max == pytest.approx(expected_rate), entry.condition_comp
        del expected_conds_up_rate[entry.condition_comp]

    assert len(expected_conds_up_rate) == 0, f"Conditions not tested: {list(sorted(expected_conds_up_rate.keys()))}"


def test_s2(transformer_skill: SkillTransformer):
    # Lapis S2
    # https://dragalialost.wiki/w/Lapis
    skill_data_base = transformer_skill.transform_attacking(109502012)

    expected_buff_count_conds = [
        Condition.SELF_BUFF_0,
        Condition.SELF_BUFF_1,
        Condition.SELF_BUFF_2,
        Condition.SELF_BUFF_3,
        Condition.SELF_BUFF_4,
        Condition.SELF_BUFF_5,
        Condition.SELF_BUFF_6,
        Condition.SELF_BUFF_7,
        Condition.SELF_BUFF_8,
        Condition.SELF_BUFF_9,
        Condition.SELF_BUFF_10,
        Condition.SELF_BUFF_15,
        Condition.SELF_BUFF_20,
        Condition.SELF_BUFF_25,
        Condition.SELF_BUFF_30,
        Condition.SELF_BUFF_35,
        Condition.SELF_BUFF_40,
        Condition.SELF_BUFF_45,
        Condition.SELF_BUFF_50,
    ]
    expected_addl_conds = [
        Condition.SELF_LAPIS_CARD_0,
        Condition.SELF_LAPIS_CARD_1,
        Condition.SELF_LAPIS_CARD_2,
        Condition.SELF_LAPIS_CARD_3,
    ]
    expected_conds_up_rate = {
        (buff_count_cond, addl_cond):
            min(
                ConditionCategories.self_buff_count.convert(buff_count_cond) * 0.05
                + ConditionCategories.self_lapis_card.convert(addl_cond) * 0.2,
                0.8
            )
        for buff_count_cond, addl_cond in product(expected_buff_count_conds, expected_addl_conds)
    }

    for conditions, boost_rate in expected_conds_up_rate.items():
        skill_data = skill_data_base.with_conditions(ConditionComposite(conditions))

        assert skill_data.hit_count == [2, 2]
        assert skill_data.hit_count_at_max == 2
        assert skill_data.total_mod == pytest.approx([12.06 * (1 + boost_rate) * 2, 15.05 * (1 + boost_rate) * 2])
        assert skill_data.total_mod_at_max == pytest.approx(15.05 * (1 + boost_rate) * 2)
        assert skill_data.mods == approx_matrix([[12.06 * (1 + boost_rate)] * 2, [15.05 * (1 + boost_rate)] * 2])
        assert skill_data.mods_at_max == pytest.approx([15.05 * (1 + boost_rate)] * 2)
        assert skill_data.max_level == 2
