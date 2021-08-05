import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_1_gauge(transformer_skill: SkillTransformer):
    # Summer Chelle
    # https://dragalialost.wiki/w/Summer_Chelle
    skill_data_base = transformer_skill.transform_attacking(107504041)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([
        26.23,
        26.78,
        27.51
    ])
    assert skill_data.total_mod_at_max == pytest.approx(27.51)
    assert skill_data.mods == approx_matrix([
        [26.23],
        [26.78],
        [27.51]
    ])
    assert skill_data.mods_at_max == pytest.approx([27.51])
    assert skill_data.max_level == 3


def test_s1_2_gauges(transformer_skill: SkillTransformer):
    # Summer Chelle
    # https://dragalialost.wiki/w/Summer_Chelle
    skill_data_base = transformer_skill.transform_attacking(107504043)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([
        52.46,
        53.56,
        55.02
    ])
    assert skill_data.total_mod_at_max == pytest.approx(55.02)
    assert skill_data.mods == approx_matrix([
        [52.46],
        [53.56],
        [55.02]
    ])
    assert skill_data.mods_at_max == pytest.approx([55.02])
    assert skill_data.max_level == 3
