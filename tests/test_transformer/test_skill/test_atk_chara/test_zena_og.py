import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s2(transformer_skill: SkillTransformer):
    # Original Zena S2
    # https://dragalialost.wiki/w/Zena
    skill_data_base = transformer_skill.transform_attacking(107505042)

    level_1_hit = 3.2
    level_1_bullet = 0.4
    level_2_hit = 4.0
    level_2_bullet = 0.5

    hits_expected = 120

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [hits_expected + 1, hits_expected + 1, 1]
    assert skill_data.hit_count_at_max == hits_expected + 1
    assert skill_data.total_mod == pytest.approx([
        level_1_hit + level_1_bullet * hits_expected,
        level_2_hit + level_2_bullet * hits_expected,
        level_2_hit
    ])
    assert skill_data.total_mod_at_max == pytest.approx(level_2_hit + level_2_bullet * hits_expected)
    assert skill_data.mods == approx_matrix([
        [level_1_hit] + [level_1_bullet] * hits_expected,
        [level_2_hit] + [level_2_bullet] * hits_expected,
        [level_2_hit]
    ])
    assert skill_data.mods_at_max == pytest.approx([level_2_hit] + [level_2_bullet] * hits_expected)
    assert skill_data.max_level == 2
