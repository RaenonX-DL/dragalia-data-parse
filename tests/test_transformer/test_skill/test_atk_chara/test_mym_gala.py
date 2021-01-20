from itertools import zip_longest

import pytest

from dlparse.enums import SkillCancelAction
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_cancel_s2_data(transformer_skill: SkillTransformer):
    # Gala Mym S2
    # https://dragalialost.gamepedia.com/Gala_Mym
    skill_data = transformer_skill.transform_attacking(105501012)

    expected_cancel_action_data = {(SkillCancelAction.MOTION_ENDS, 1.63333344)}

    main_expected = [set(expected_cancel_action_data)] * 4
    main_actual = [
        {(cancel_unit.action, cancel_unit.time) for cancel_unit in cancel_unit_lv}
        for cancel_unit_lv in skill_data.cancel_unit_mtx
    ]

    for expected_lv, actual_lv in zip_longest(main_expected, main_actual):
        diff = expected_lv.symmetric_difference(actual_lv)
        assert len(diff) == 0, diff


def test_s2(transformer_skill: SkillTransformer):
    # Gala Mym S2
    # https://dragalialost.gamepedia.com/Gala_Mym
    skill_data_base = transformer_skill.transform_attacking(105501012)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        4.675 * 4,
        5.175 * 4,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(5.175 * 4)
    assert skill_data.mods == approx_matrix([
        [4.675] * 4,
        [5.175] * 4,
    ])
    assert skill_data.mods_at_max == pytest.approx([5.175] * 4)
    assert skill_data.max_level == 2


def test_s2_shapeshifted(transformer_skill: SkillTransformer):
    # Gala Mym S2
    # https://dragalialost.gamepedia.com/Gala_Mym
    skill_data_base = transformer_skill.transform_attacking(105501013)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        5.62 * 4,
        6.22 * 4,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(6.22 * 4)
    assert skill_data.mods == approx_matrix([
        [5.62] * 4,
        [6.22] * 4,
    ])
    assert skill_data.mods_at_max == pytest.approx([6.22] * 4)
    assert skill_data.max_level == 2
