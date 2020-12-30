import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1(transformer_skill: SkillTransformer):
    # Wedding Aoi S1
    # https://dragalialost.gamepedia.com/Wedding_Aoi
    skill_data_base = transformer_skill.transform_attacking(103503011)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [5, 5, 5]
    assert skill_data.hit_count_at_max == 5
    assert skill_data.total_mod == pytest.approx([
        2.926 * 4 + 11.682,
        3.08 * 4 + 12.276,
        3.234 * 4 + 12.892,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3.234 * 4 + 12.892)
    assert skill_data.mods == approx_matrix([
        [2.926] * 4 + [11.682],
        [3.08] * 4 + [12.276],
        [3.234] * 4 + [12.892]
    ])
    assert skill_data.mods_at_max == pytest.approx([3.234] * 4 + [12.892])
    assert skill_data.max_level == 3
