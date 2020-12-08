import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1(transformer_skill: SkillTransformer):
    # Lin You S1
    # https://dragalialost.gamepedia.com/Lin_You
    skill_data_base = transformer_skill.transform_attacking(104503011)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [6, 6, 6, 8]
    assert skill_data.hit_count_at_max == 8
    assert skill_data.total_mod == pytest.approx([
        1.76 * 6,
        1.96 * 6,
        2.18 * 6,
        2.42 * 8
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.42 * 8)
    assert skill_data.mods == approx_matrix([
        [1.76] * 6,
        [1.96] * 6,
        [2.18] * 6,
        [2.42] * 8
    ])
    assert skill_data.mods_at_max == pytest.approx([2.42] * 8)
    assert skill_data.max_level == 4


def test_s1_heaven(transformer_skill: SkillTransformer):
    # Lin You S1 @ Heaven's Breath
    # https://dragalialost.gamepedia.com/Lin_You
    skill_data_base = transformer_skill.transform_attacking(104503013)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [9, 9, 9, 10]
    assert skill_data.hit_count_at_max == 10
    assert skill_data.total_mod == pytest.approx([
        1.76 * 9,
        1.96 * 9,
        2.18 * 9,
        2.42 * 10
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.42 * 10)
    assert skill_data.mods == approx_matrix([
        [1.76] * 9,
        [1.96] * 9,
        [2.18] * 9,
        [2.42] * 10
    ])
    assert skill_data.mods_at_max == pytest.approx([2.42] * 10)
    assert skill_data.max_level == 4
