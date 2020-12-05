import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1(transformer_skill: SkillTransformer):
    # Incognito Nefaria S1
    # https://dragalialost.gamepedia.com/Incognito_Nefaria
    skill_data_base = transformer_skill.transform_attacking(107501031)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [17, 17, 17]
    assert skill_data.hit_count_at_max == 17
    assert skill_data.total_mod == pytest.approx([
        1.11 * 17,
        1.21 * 17,
        1.32 * 17
    ])
    assert skill_data.total_mod_at_max == pytest.approx(1.32 * 17)
    assert skill_data.mods == approx_matrix([
        [1.11] * 17,
        [1.21] * 17,
        [1.32] * 17
    ])
    assert skill_data.mods_at_max == pytest.approx([1.32] * 17)
    assert skill_data.max_level == 3
