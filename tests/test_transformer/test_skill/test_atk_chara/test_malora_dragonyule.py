import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s2(transformer_skill: SkillTransformer):
    # Dragonyule Malora S2
    # https://dragalialost.gamepedia.com/Dragonyule_Malora
    skill_data_base = transformer_skill.transform_attacking(104504022)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([3.86 * 3, 4.32 * 3])
    assert skill_data.total_mod_at_max == pytest.approx(4.32 * 3)
    assert skill_data.mods == approx_matrix([[3.86] * 3, [4.32] * 3])
    assert skill_data.mods_at_max == pytest.approx([4.32] * 3)
    assert skill_data.max_level == 2

    # Target DEF down
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_DEF_DOWN))

    assert skill_data.hit_count == [3, 3]
    assert skill_data.hit_count_at_max == 3
    assert skill_data.total_mod == pytest.approx([6.948 * 3, 7.776 * 3])
    assert skill_data.total_mod_at_max == pytest.approx(7.776 * 3)
    assert skill_data.mods == approx_matrix([[6.948] * 3, [7.776] * 3])
    assert skill_data.mods_at_max == pytest.approx([7.776] * 3)
    assert skill_data.max_level == 2
