import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_normal(transformer_skill: SkillTransformer):
    # Ilia S1
    # https://dragalialost.gamepedia.com/Ilia
    skill_data_base = transformer_skill.transform_attacking(109504011)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [10, 10, 10]
    assert skill_data.hit_count_at_max == 10
    assert skill_data.total_mod == pytest.approx([
        1.52 * 10,
        1.69 * 10,
        1.88 * 10
    ])
    assert skill_data.total_mod_at_max == pytest.approx(1.88 * 10)
    assert skill_data.mods == approx_matrix([
        [1.52] * 10,
        [1.69] * 10,
        [1.88] * 10
    ])
    assert skill_data.mods_at_max == pytest.approx([1.88] * 10)
    assert skill_data.max_level == 3


def test_s1_alchemy(transformer_skill: SkillTransformer):
    # Ilia S1 @ Alchemy
    # https://dragalialost.gamepedia.com/Ilia
    skill_data_base = transformer_skill.transform_attacking(109504013)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [6, 6, 6]
    assert skill_data.hit_count_at_max == 6
    assert skill_data.total_mod == pytest.approx([
        2.82 * 6,
        3.13 * 6,
        3.48 * 6
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3.48 * 6)
    assert skill_data.mods == approx_matrix([
        [2.82] * 6,
        [3.13] * 6,
        [3.48] * 6
    ])
    assert skill_data.mods_at_max == pytest.approx([3.48] * 6)
    assert skill_data.max_level == 3


def test_s2_alchemy(transformer_skill: SkillTransformer):
    # Ilia S2 @ Alchemy
    # https://dragalialost.gamepedia.com/Ilia
    skill_data_base = transformer_skill.transform_attacking(109504014)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [2, 2, 0]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        21.19 + 2.12,
        23.54 + 2.35,
        0
    ])
    assert skill_data.total_mod_at_max == pytest.approx(23.54 + 2.35)
    assert skill_data.mods == approx_matrix([
        [2.12, 21.19],
        [2.35, 23.54],
        []
    ])
    assert skill_data.mods_at_max == pytest.approx([2.35, 23.54])
    assert skill_data.max_level == 2
