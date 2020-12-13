import pytest

from dlparse.transformer import SkillTransformer


def test_elisanne_s1(transformer_skill: SkillTransformer):
    # Elisanne S1
    # https://dragalialost.gamepedia.com/Elisanne
    skill_data_base = transformer_skill.transform_attacking(105402011)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [0, 0, 0, 5]
    assert skill_data.hit_count_at_max == 5
    assert skill_data.total_mod == pytest.approx([0, 0, 0, 7.5])
    assert skill_data.total_mod_at_max == pytest.approx(7.5)
    assert skill_data.mods == [[], [], [], [1.5] * 5]
    assert skill_data.mods_at_max == [1.5] * 5
    assert skill_data.max_level == 4
