import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries_s2(transformer_skill: SkillTransformer):
    # Mitsuhide
    # https://dragalialost.gamepedia.com/Mitsuhide
    skill_data = transformer_skill.transform_attacking(103504022)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        SkillConditionComposite(SkillCondition.COMBO_0): 13.56 * 1.00,
        SkillConditionComposite(SkillCondition.COMBO_5): 13.56 * 1.05,
        SkillConditionComposite(SkillCondition.COMBO_10): 13.56 * 1.10,
        SkillConditionComposite(SkillCondition.COMBO_15): 13.56 * 1.20,
        SkillConditionComposite(SkillCondition.COMBO_20): 13.56 * 1.30,
        SkillConditionComposite(SkillCondition.COMBO_25): 13.56 * 1.40,
        SkillConditionComposite(SkillCondition.COMBO_30): 13.56 * 1.50,
    }

    expected = set(expected_addl_at_max.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        assert \
            pytest.approx(expected_addl_at_max[entry.condition_comp]) == entry.total_mod_at_max, \
            entry.condition_comp
        del expected_addl_at_max[entry.condition_comp]

    assert len(expected_addl_at_max) == 0, f"Conditions not tested: {set(expected_addl_at_max.keys())}"


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
