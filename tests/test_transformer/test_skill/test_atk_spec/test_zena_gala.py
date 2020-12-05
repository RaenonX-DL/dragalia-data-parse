import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s2(transformer_skill: SkillTransformer):
    # Gala Zena S2
    # https://dragalialost.gamepedia.com/Gala_Zena
    skill_data_base = transformer_skill.transform_attacking(108504022)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [10, 10]
    assert skill_data.hit_count_at_max == 10
    assert skill_data.total_mod == pytest.approx([
        0.45 * 5 + 3.15 * 5,
        0.5 * 5 + 3.5 * 5
    ])
    assert skill_data.total_mod_at_max == pytest.approx(0.5 * 5 + 3.5 * 5)
    assert skill_data.mods == approx_matrix([
        [0.45] * 5 + [3.15] * 5,
        [0.5] * 5 + [3.5] * 5
    ])
    assert skill_data.mods_at_max == pytest.approx([0.5] * 5 + [3.5] * 5)
    assert skill_data.max_level == 2
