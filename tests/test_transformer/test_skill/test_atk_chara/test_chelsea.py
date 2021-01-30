import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_normal(transformer_skill: SkillTransformer):
    # Chelsea S1
    # https://dragalialost.wiki/w/Chelsea
    skill_data_base = transformer_skill.transform_attacking(106501021)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [7, 7, 7]
    assert skill_data.hit_count_at_max == 7
    assert skill_data.total_mod == pytest.approx([
        1.21 * 7,
        1.34 * 7,
        1.5 * 7
    ])
    assert skill_data.total_mod_at_max == pytest.approx(1.5 * 7)
    assert skill_data.mods == approx_matrix([
        [1.21] * 7,
        [1.34] * 7,
        [1.5] * 7
    ])
    assert skill_data.mods_at_max == pytest.approx([1.5] * 7)
    assert skill_data.max_level == 3


def test_s1_obsession(transformer_skill: SkillTransformer):
    # Chelsea S1 @ Obsession
    # https://dragalialost.wiki/w/Chelsea
    skill_data_base = transformer_skill.transform_attacking(106501023)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [7, 7, 7]
    assert skill_data.hit_count_at_max == 7
    assert skill_data.total_mod == pytest.approx([
        1.76 * 7,
        1.952 * 7,
        2.176 * 7
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.176 * 7)
    assert skill_data.mods == approx_matrix([
        [1.76] * 7,
        [1.952] * 7,
        [2.176] * 7
    ])
    assert skill_data.mods_at_max == pytest.approx([2.176] * 7)
    assert skill_data.max_level == 3
