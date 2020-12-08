import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_p2(transformer_skill: SkillTransformer):
    # Xander S1 P2
    # https://dragalialost.gamepedia.com/Xander
    skill_data_base = transformer_skill.transform_attacking(101502013)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [0, 0, 0, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([0, 0, 0, 16.74])
    assert skill_data.total_mod_at_max == pytest.approx(16.74)
    assert skill_data.mods == approx_matrix([[], [], [], [16.74]])
    assert skill_data.mods_at_max == pytest.approx([16.74])
    assert skill_data.max_level == 4


def test_s1_p3(transformer_skill: SkillTransformer):
    # Xander S1 P3
    # https://dragalialost.gamepedia.com/Xander
    skill_data_base = transformer_skill.transform_attacking(101502014)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [0, 0, 0, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([0, 0, 0, 16.8])
    assert skill_data.total_mod_at_max == pytest.approx(16.8)
    assert skill_data.mods == approx_matrix([[], [], [], [16.8]])
    assert skill_data.mods_at_max == pytest.approx([16.8])
    assert skill_data.max_level == 4
