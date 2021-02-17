import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_arsene(transformer_skill: SkillTransformer):
    # Joker S1 (Arsene summoned)
    # https://dragalialost.wiki/w/Joker
    # Action ID affiliated to 103505054 does not have any meaningful damage modifier
    # Summoning Arsene is handled as shapeshifting (Unique Dragon ID: 29900010)
    skill_data_base = transformer_skill.transform_attacking(299000102)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([
        25.7,
        30.3
    ])
    assert skill_data.total_mod_at_max == pytest.approx(30.3)
    assert skill_data.mods == approx_matrix([
        [25.7],
        [30.3]
    ])
    assert skill_data.mods_at_max == pytest.approx([30.3])
    assert skill_data.max_level == 2
