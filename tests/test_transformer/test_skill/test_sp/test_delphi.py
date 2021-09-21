import pytest

from dlparse.transformer import SkillTransformer


def test_s1_sp_gradual_fill(transformer_skill: SkillTransformer):
    # Delphi S1
    # https://dragalialost.wiki/w/Delphi
    skill_data = transformer_skill.transform_attacking(103505021)

    assert skill_data.sp_gradual_fill_pct == pytest.approx([8.0] * 4)


def test_s2_sp_gradual_fill(transformer_skill: SkillTransformer):
    # Delphi S2
    # https://dragalialost.wiki/w/Delphi
    skill_data = transformer_skill.transform_attacking(103505022)

    assert skill_data.sp_gradual_fill_pct == pytest.approx([5.0] * 3)
