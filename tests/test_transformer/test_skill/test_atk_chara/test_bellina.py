import pytest

from dlparse.transformer import SkillTransformer


def test_s1(transformer_skill: SkillTransformer):
    # Bellina S1
    # https://dragalialost.gamepedia.com/Bellina
    skill_data_base = transformer_skill.transform_attacking(103505033)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [5, 5, 5]
    assert skill_data.hit_count_at_max == 5
    assert skill_data.total_mod == pytest.approx([1.63 * 5, 1.81 * 5, 2.02 * 5])
    assert skill_data.total_mod_at_max == pytest.approx(2.02 * 5)
    assert skill_data.mods == [[1.63] * 5, [1.81] * 5, [2.02] * 5]
    assert skill_data.mods_at_max == [2.02] * 5
    assert skill_data.max_level == 3
