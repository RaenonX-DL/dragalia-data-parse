import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1(transformer_skill: SkillTransformer):
    # Formal Joachim S1
    # https://dragalialost.gamepedia.com/Formal_Joachim
    skill_data_base = transformer_skill.transform_attacking(109503011)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([8.19, 9.11, 10.12])
    assert skill_data.total_mod_at_max == pytest.approx(10.12)
    assert skill_data.mods == approx_matrix([[8.19], [9.11], [10.12]])
    assert skill_data.mods_at_max == pytest.approx([10.12])
    assert skill_data.max_level == 3


def test_s1_explode(transformer_skill: SkillTransformer):
    # Formal Joachim S1 @ Aced (S2-S1)
    # https://dragalialost.gamepedia.com/Formal_Joachim
    skill_data_base = transformer_skill.transform_attacking(109503011)

    # Cancels S2
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.CANCELS_FJOACHIM_S2))

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([16.72, 18.58, 20.64])
    assert skill_data.total_mod_at_max == pytest.approx(20.64)
    assert skill_data.mods == approx_matrix([[16.72], [18.58], [20.64]])
    assert skill_data.mods_at_max == pytest.approx([20.64])
    assert skill_data.max_level == 3
