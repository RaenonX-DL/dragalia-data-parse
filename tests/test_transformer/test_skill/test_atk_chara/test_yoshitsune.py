import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_normal(transformer_skill: SkillTransformer):
    # Yoshitsune
    # https://dragalialost.gamepedia.com/Yoshitsune
    skill_data_base = transformer_skill.transform_attacking(109502021)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [5, 5, 5]
    assert skill_data.hit_count_at_max == 5
    assert skill_data.total_mod == pytest.approx([5.95, 8.9, 10.65])
    assert skill_data.total_mod_at_max == pytest.approx(10.65)
    assert skill_data.mods == approx_matrix([[1.19] * 5, [1.78] * 5, [2.13] * 5])
    assert skill_data.mods_at_max == pytest.approx([2.13] * 5)
    assert skill_data.max_level == 3


def test_s1_counter(transformer_skill: SkillTransformer):
    # Yoshitsune
    # https://dragalialost.gamepedia.com/Yoshitsune
    skill_data_base = transformer_skill.transform_attacking(109502021)

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.COUNTER_RED_ATTACK))

    assert skill_data.hit_count == [7, 7, 7]
    assert skill_data.hit_count_at_max == 7
    assert skill_data.total_mod == pytest.approx([17.42, 22.56, 26.47])
    assert skill_data.total_mod_at_max == pytest.approx(26.47)
    assert skill_data.mods == approx_matrix([
        [0.09, 11.38] + [1.19] * 5,
        [0.1, 13.56] + [1.78] * 5,
        [0.1, 15.72] + [2.13] * 5
    ])
    assert skill_data.mods_at_max == pytest.approx([0.1, 15.72] + [2.13] * 5)
    assert skill_data.max_level == 3
