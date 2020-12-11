import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s2(transformer_skill: SkillTransformer):
    # Mitsuhide
    # https://dragalialost.gamepedia.com/Mitsuhide
    skill_data_base = transformer_skill.transform_attacking(103504022)

    combo_dmg_bonus = {
        SkillConditionComposite(SkillCondition.COMBO_0): 1,
        SkillConditionComposite(SkillCondition.COMBO_5): 1.05,
        SkillConditionComposite(SkillCondition.COMBO_10): 1.10,
        SkillConditionComposite(SkillCondition.COMBO_15): 1.20,
        SkillConditionComposite(SkillCondition.COMBO_20): 1.30,
        SkillConditionComposite(SkillCondition.COMBO_25): 1.40,
        SkillConditionComposite(SkillCondition.COMBO_30): 1.50,
    }

    for condition, dmg_rate in combo_dmg_bonus.items():
        skill_data = skill_data_base.with_conditions(condition)

        assert skill_data.hit_count == [1, 1]
        assert skill_data.hit_count_at_max == 1
        assert skill_data.total_mod == pytest.approx([12.21 * dmg_rate, 13.56 * dmg_rate])
        assert skill_data.total_mod_at_max == pytest.approx(13.56 * dmg_rate)
        assert skill_data.mods == approx_matrix([[12.21 * dmg_rate], [13.56 * dmg_rate]])
        assert skill_data.mods_at_max == pytest.approx([13.56 * dmg_rate])
        assert skill_data.max_level == 2
