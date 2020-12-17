from itertools import product

import pytest

from dlparse.enums import SkillCondition, SkillConditionCategories, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries_s2(transformer_skill: SkillTransformer):
    # Lapis S2
    # https://dragalialost.gamepedia.com/Lapis

    skill_data = transformer_skill.transform_attacking(109502012, is_exporting=True)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_conds = [
        SkillCondition.SELF_LAPIS_CARD_0,
        SkillCondition.SELF_LAPIS_CARD_1,
        SkillCondition.SELF_LAPIS_CARD_2,
        SkillCondition.SELF_LAPIS_CARD_3,
    ]
    expected_conds_up_rate = {
        SkillConditionComposite(addl_cond): min(SkillConditionCategories.self_lapis_card.convert(addl_cond) * 0.2, 0.8)
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
        SkillCondition.SELF_BUFF_0,
        SkillCondition.SELF_BUFF_1,
        SkillCondition.SELF_BUFF_2,
        SkillCondition.SELF_BUFF_3,
        SkillCondition.SELF_BUFF_4,
        SkillCondition.SELF_BUFF_5,
        SkillCondition.SELF_BUFF_6,
        SkillCondition.SELF_BUFF_7,
        SkillCondition.SELF_BUFF_8,
        SkillCondition.SELF_BUFF_9,
        SkillCondition.SELF_BUFF_10,
        SkillCondition.SELF_BUFF_15,
        SkillCondition.SELF_BUFF_20,
        SkillCondition.SELF_BUFF_25,
        SkillCondition.SELF_BUFF_30,
        SkillCondition.SELF_BUFF_35,
        SkillCondition.SELF_BUFF_40,
        SkillCondition.SELF_BUFF_45,
        SkillCondition.SELF_BUFF_50,
    ]
    expected_addl_conds = [
        SkillCondition.SELF_LAPIS_CARD_0,
        SkillCondition.SELF_LAPIS_CARD_1,
        SkillCondition.SELF_LAPIS_CARD_2,
        SkillCondition.SELF_LAPIS_CARD_3,
    ]
    expected_conds_up_rate = {
        SkillConditionComposite([buff_count_cond, addl_cond]):
            min(
                SkillConditionCategories.self_buff_count.convert(buff_count_cond) * 0.05
                + SkillConditionCategories.self_lapis_card.convert(addl_cond) * 0.2,
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
    # https://dragalialost.gamepedia.com/Lapis
    skill_data_base = transformer_skill.transform_attacking(109502012)

    expected_buff_count_conds = [
        SkillCondition.SELF_BUFF_0,
        SkillCondition.SELF_BUFF_1,
        SkillCondition.SELF_BUFF_2,
        SkillCondition.SELF_BUFF_3,
        SkillCondition.SELF_BUFF_4,
        SkillCondition.SELF_BUFF_5,
        SkillCondition.SELF_BUFF_6,
        SkillCondition.SELF_BUFF_7,
        SkillCondition.SELF_BUFF_8,
        SkillCondition.SELF_BUFF_9,
        SkillCondition.SELF_BUFF_10,
        SkillCondition.SELF_BUFF_15,
        SkillCondition.SELF_BUFF_20,
        SkillCondition.SELF_BUFF_25,
        SkillCondition.SELF_BUFF_30,
        SkillCondition.SELF_BUFF_35,
        SkillCondition.SELF_BUFF_40,
        SkillCondition.SELF_BUFF_45,
        SkillCondition.SELF_BUFF_50,
    ]
    expected_addl_conds = [
        SkillCondition.SELF_LAPIS_CARD_0,
        SkillCondition.SELF_LAPIS_CARD_1,
        SkillCondition.SELF_LAPIS_CARD_2,
        SkillCondition.SELF_LAPIS_CARD_3,
    ]
    expected_conds_up_rate = {
        (buff_count_cond, addl_cond):
            min(
                SkillConditionCategories.self_buff_count.convert(buff_count_cond) * 0.05
                + SkillConditionCategories.self_lapis_card.convert(addl_cond) * 0.2,
                0.8
            )
        for buff_count_cond, addl_cond in product(expected_buff_count_conds, expected_addl_conds)
    }

    for conditions, boost_rate in expected_conds_up_rate.items():
        skill_data = skill_data_base.with_conditions(SkillConditionComposite(conditions))

        assert skill_data.hit_count == [2, 2]
        assert skill_data.hit_count_at_max == 2
        assert skill_data.total_mod == pytest.approx([12.06 * (1 + boost_rate) * 2, 15.05 * (1 + boost_rate) * 2])
        assert skill_data.total_mod_at_max == pytest.approx(15.05 * (1 + boost_rate) * 2)
        assert skill_data.mods == approx_matrix([[12.06 * (1 + boost_rate)] * 2, [15.05 * (1 + boost_rate)] * 2])
        assert skill_data.mods_at_max == pytest.approx([15.05 * (1 + boost_rate)] * 2)
        assert skill_data.max_level == 2
