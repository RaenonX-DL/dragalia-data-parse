import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s2_does_not_have_zero_mods(transformer_skill: SkillTransformer):
    # Shooter Sarisse S2
    # https://dragalialost.wiki/w/Sharpshooter_Sarisse
    skill_data = transformer_skill.transform_attacking(109502032)

    assert skill_data.has_non_zero_mods


def test_s2(transformer_skill: SkillTransformer):
    # Shooter Sarisse S2
    # https://dragalialost.wiki/w/Sharpshooter_Sarisse
    skill_data_base = transformer_skill.transform_attacking(109502032)

    # 991210, 991211, 991212 are the variants of her S2
    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.PROB_33), action_id=991210)

    assert skill_data.hit_count == [5, 5]
    assert skill_data.hit_count_at_max == 5
    assert skill_data.total_mod == pytest.approx([
        3.06 * 1 + 1.39 * 4,
        3.30 * 1 + 1.49 * 4
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3.30 * 1 + 1.49 * 4)
    assert skill_data.mods == approx_matrix([
        [1.39] * 4 + [3.06] * 1,
        [1.49] * 4 + [3.30] * 1
    ])
    assert skill_data.mods_at_max == pytest.approx([1.49] * 4 + [3.30] * 1)
    assert skill_data.max_level == 2
