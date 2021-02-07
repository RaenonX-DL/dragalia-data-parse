from itertools import zip_longest

from dlparse.enums import SkillCancelAction
from dlparse.transformer import SkillTransformer


def test_s1_cancel_data(transformer_skill: SkillTransformer):
    # Wedding Elisanne S1
    # https://dragalialost.wiki/w/Wedding_Elisanne
    skill_data = transformer_skill.transform_attacking(101503021).with_conditions()

    expected_cancel_action_data = {(SkillCancelAction.MOTION_ENDS, 1.80000007)}

    main_expected = [set(expected_cancel_action_data)] * 4
    main_actual = [
        {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
        for cancel_unit_lv in skill_data.cancel_unit_mtx
    ]

    for expected_lv, actual_lv in zip_longest(main_expected, main_actual):
        diff = expected_lv.symmetric_difference(actual_lv)
        assert len(diff) == 0, diff


def test_s2_cancel_data(transformer_skill: SkillTransformer):
    # Wedding Elisanne S2
    # https://dragalialost.wiki/w/Wedding_Elisanne
    skill_data = transformer_skill.transform_attacking(101503022).with_conditions()

    expected_cancel_action_data = {(SkillCancelAction.MOTION_ENDS, 0.966666639)}

    main_expected = [set(expected_cancel_action_data)] * 4
    main_actual = [
        {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
        for cancel_unit_lv in skill_data.cancel_unit_mtx
    ]

    for expected_lv, actual_lv in zip_longest(main_expected, main_actual):
        diff = expected_lv.symmetric_difference(actual_lv)
        assert len(diff) == 0, diff
