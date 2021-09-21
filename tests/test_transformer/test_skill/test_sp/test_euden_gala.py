import pytest

from dlparse.transformer import SkillTransformer


def test_s2_sp_gradual_fill(transformer_skill: SkillTransformer):
    # Gala Euden S2
    # https://dragalialost.wiki/w/Gala_Prince
    skill_data = transformer_skill.transform_attacking(101504032)

    assert skill_data.sp_gradual_fill_pct == pytest.approx([3.2] * 3)
