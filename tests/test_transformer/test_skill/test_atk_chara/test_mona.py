from itertools import zip_longest

import pytest

from dlparse.enums import Condition, ConditionComposite, SkillCancelAction
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_zorro_cancel_data(transformer_skill: SkillTransformer):
    # Mona S1 (Zorro summoned)
    # https://dragalialost.wiki/w/Mona
    skill_data = transformer_skill.transform_attacking(299000121)
    skill_data = skill_data.with_conditions(ConditionComposite(Condition.PROB_75))

    expected_cancel_action_data = {(SkillCancelAction.MOTION_ENDS, 1.9666667)}

    main_expected = [set(expected_cancel_action_data)] * 4
    main_actual = [
        {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
        for cancel_unit_lv in skill_data.cancel_unit_mtx
    ]

    for expected_lv, actual_lv in zip_longest(main_expected, main_actual):
        diff = expected_lv.symmetric_difference(actual_lv)
        assert len(diff) == 0, diff


def test_s1_zorro_enhanced_cancel_data(transformer_skill: SkillTransformer):
    # Mona S1 (Zorro summoned & enhanced)
    # https://dragalialost.wiki/w/Mona
    skill_data = transformer_skill.transform_attacking(299000121)
    skill_data = skill_data.with_conditions(ConditionComposite(Condition.PROB_25))

    expected_cancel_action_data = {(SkillCancelAction.MOTION_ENDS, 1.9666667)}

    main_expected = [set(expected_cancel_action_data)] * 4
    main_actual = [
        {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
        for cancel_unit_lv in skill_data.cancel_unit_mtx
    ]

    for expected_lv, actual_lv in zip_longest(main_expected, main_actual):
        diff = expected_lv.symmetric_difference(actual_lv)
        assert len(diff) == 0, diff


def test_s1(transformer_skill: SkillTransformer):
    # Mona S1
    # https://dragalialost.wiki/w/Mona
    skill_data_base = transformer_skill.transform_attacking(101503041)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [10, 10, 10]
    assert skill_data.hit_count_at_max == 10
    assert skill_data.total_mod == pytest.approx([
        1.82 * 10,
        2.03 * 10,
        2.25 * 10
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.25 * 10)
    assert skill_data.mods == approx_matrix([
        [1.82] * 10,
        [2.03] * 10,
        [2.25] * 10
    ])
    assert skill_data.mods_at_max == pytest.approx([2.25] * 10)
    assert skill_data.max_level == 3


def test_s1_zorro_no_prob(transformer_skill: SkillTransformer):
    # Mona S1 (Zorro summoned & no probability condition - should not contain any hit data)
    # https://dragalialost.wiki/w/Mona
    # Action ID affiliated to 101503043 does not have any meaningful damage modifier
    # Summoning Zorro is handled as shapeshifting (Unique Dragon ID: 29900012)
    skill_data_base = transformer_skill.transform_attacking(299000121)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [0, 0, 0]
    assert skill_data.hit_count_at_max == 0
    assert skill_data.total_mod == pytest.approx([0, 0, 0])
    assert skill_data.total_mod_at_max == pytest.approx(0)
    assert skill_data.mods == approx_matrix([[], [], []])
    assert skill_data.mods_at_max == pytest.approx([])
    assert skill_data.max_level == 3


def test_s1_zorro(transformer_skill: SkillTransformer):
    # Mona S1 (Zorro summoned)
    # https://dragalialost.wiki/w/Mona
    # Action ID affiliated to 101503043 does not have any meaningful damage modifier
    # Summoning Zorro is handled as shapeshifting (Unique Dragon ID: 29900012)
    skill_data_base = transformer_skill.transform_attacking(299000121)

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.PROB_75))

    assert skill_data.hit_count == [3, 3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([
        6.68 * 3,
        7.43 * 3,
        8.25 * 3
    ])
    assert skill_data.total_mod_at_max == pytest.approx(8.25 * 3)
    assert skill_data.mods == approx_matrix([
        [6.68] * 3,
        [7.43] * 3,
        [8.25] * 3
    ])
    assert skill_data.mods_at_max == pytest.approx([8.25] * 3)
    assert skill_data.max_level == 3


def test_s1_zorro_enhanced(transformer_skill: SkillTransformer):
    # Mona S1 (Zorro summoned & enhanced)
    # https://dragalialost.wiki/w/Mona
    # Action ID affiliated to 101503043 does not have any meaningful damage modifier
    # Summoning Zorro is handled as shapeshifting (Unique Dragon ID: 29900012)
    skill_data_base = transformer_skill.transform_attacking(299000121)

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.PROB_25))

    assert skill_data.hit_count == [5, 5, 5]
    assert skill_data.hit_count_at_max == 5
    assert skill_data.total_mod == pytest.approx([
        4.05 * 5,
        4.50 * 5,
        5.00 * 5
    ])
    assert skill_data.total_mod_at_max == pytest.approx(5.00 * 5)
    assert skill_data.mods == approx_matrix([
        [4.05] * 5,
        [4.50] * 5,
        [5.00] * 5
    ])
    assert skill_data.mods_at_max == pytest.approx([5.00] * 5)
    assert skill_data.max_level == 3


def test_s2(transformer_skill: SkillTransformer):
    # Mona S2
    # https://dragalialost.wiki/w/Mona
    skill_data_base = transformer_skill.transform_attacking(101503042)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        5.4 * 4,
        6.0 * 4
    ])
    assert skill_data.total_mod_at_max == pytest.approx(6.0 * 4)
    assert skill_data.mods == approx_matrix([
        [5.4] * 4,
        [6.0] * 4
    ])
    assert skill_data.mods_at_max == pytest.approx([6.0] * 4)
    assert skill_data.max_level == 2


def test_s2_zorro(transformer_skill: SkillTransformer):
    # Mona S2 (Zorro summoned)
    # https://dragalialost.wiki/w/Mona
    skill_data_base = transformer_skill.transform_attacking(299000122)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [5, 5]
    assert skill_data.hit_count_at_max == 5
    assert skill_data.total_mod == pytest.approx([
        5.4 * 5,
        6.0 * 5
    ])
    assert skill_data.total_mod_at_max == pytest.approx(6.0 * 5)
    assert skill_data.mods == approx_matrix([
        [5.4] * 5,
        [6.0] * 5
    ])
    assert skill_data.mods_at_max == pytest.approx([6.0] * 5)
    assert skill_data.max_level == 2


def test_ss(transformer_skill: SkillTransformer):
    # Mona S2 (as SS)
    # https://dragalialost.wiki/w/Mona
    skill_data_base = transformer_skill.transform_attacking(101503045)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        5.4 * 4,
        6.0 * 4
    ])
    assert skill_data.total_mod_at_max == pytest.approx(6.0 * 4)
    assert skill_data.mods == approx_matrix([
        [5.4] * 4,
        [6.0] * 4
    ])
    assert skill_data.mods_at_max == pytest.approx([6.0] * 4)
    assert skill_data.max_level == 2
