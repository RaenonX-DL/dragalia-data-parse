import pytest

from dlparse.enums import SkillCondition
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_label_has_whitespaces(transformer_skill: SkillTransformer):
    """
    The text label of the action of Xander S2 (Lv 3) contains a whitespace at the end of the action label.

    Expected: ``SWD_004_04_H02_LV01``
    Actual:   ``SWD_004_04_H02_LV01 ``
    """
    # Xander S2
    # https://dragalialost.gamepedia.com/Xander
    skill_data_base = transformer_skill.transform_attacking(101502012)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [3, 3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([4.906 * 3, 5.456 * 3, 5.566 * 3])
    assert skill_data.total_mod_at_max == pytest.approx(5.566 * 3)
    assert skill_data.mods == [[4.906] * 3, [5.456] * 3, [5.566] * 3]
    assert skill_data.mods_at_max == [5.566] * 3
    assert skill_data.max_available_level == 3

    # With buffs
    condition_to_dmg_up_rate = {
        (SkillCondition.SELF_BUFF_0,): 1 + 0,
        (SkillCondition.SELF_BUFF_10,): 1 + 0.05 * 10,
        (SkillCondition.SELF_BUFF_20,): 1 + 0.05 * 20,
        (SkillCondition.SELF_BUFF_25,): 1 + 0.05 * 25,
        (SkillCondition.SELF_BUFF_30,): 1 + 0.05 * 30,
        (SkillCondition.SELF_BUFF_35,): 1 + 0.05 * 35,
        (SkillCondition.SELF_BUFF_40,): 1 + 0.05 * 40,
        (SkillCondition.SELF_BUFF_45,): 1 + 0.05 * 45,
        (SkillCondition.SELF_BUFF_50,): 1 + 0.05 * 50,
    }

    for conditions, boost_rate in condition_to_dmg_up_rate.items():
        skill_data = skill_data_base.with_conditions(*conditions)

        assert skill_data.hit_count == [3, 3, 3]
        assert skill_data.hit_count_at_max == 3
        assert skill_data.total_mod == pytest.approx([
            4.906 * 3,
            5.456 * 3,
            5.566 * 3 * boost_rate
        ])
        assert skill_data.total_mod_at_max == pytest.approx(5.566 * 3 * boost_rate)
        assert skill_data.mods == approx_matrix([
            [4.906] * 3,
            [5.456] * 3,
            [5.566 * boost_rate] * 3
        ])
        assert skill_data.mods_at_max == [5.566 * boost_rate] * 3
        assert skill_data.max_available_level == 3
