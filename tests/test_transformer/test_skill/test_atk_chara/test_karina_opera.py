from itertools import zip_longest

from dlparse.enums import SkillCancelAction
from dlparse.transformer import SkillTransformer


def test_s1_cancel_data(transformer_skill: SkillTransformer):
    # Opera Karina S1
    # https://dragalialost.wiki/w/Opera_Karina
    skill_data = transformer_skill.transform_attacking(106505041).with_conditions()

    expected_cancel_action_data = {
        (SkillCancelAction.ANY_ACTION, 7),
        (SkillCancelAction.ROLL, 3.33333325)
    }

    main_expected = [set(expected_cancel_action_data)] * 4
    main_actual = [
        {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
        for cancel_unit_lv in skill_data.cancel_unit_mtx
    ]

    for expected_lv, actual_lv in zip_longest(main_expected, main_actual):
        diff = expected_lv.symmetric_difference(actual_lv)
        assert len(diff) == 2, diff


def test_s1_cancel_entries(transformer_skill: SkillTransformer):
    # Opera Karina S1
    # https://dragalialost.wiki/w/Opera_Karina
    skill_data = transformer_skill.transform_attacking(106505041)

    expected_cancel_action_data = {
        (SkillCancelAction.ANY_ACTION, 7),
        (SkillCancelAction.ROLL, 3.33333325)
    }

    for entry in skill_data.get_all_possible_entries():
        entry_expected = [set(expected_cancel_action_data)] * 4
        entry_actual = [
            {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
            for cancel_unit_lv in entry.cancel_unit_mtx
        ]

        for expected_lv, actual_lv in zip_longest(entry_expected, entry_actual):
            diff = expected_lv.symmetric_difference(actual_lv)
            assert len(diff) == 2, diff
