import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.transformer import SkillTransformer


def test_seimei_s2_iter_entries(transformer_skill: SkillTransformer):
    # Seimei
    # https://dragalialost.wiki/w/Seimei
    skill_data = transformer_skill.transform_attacking(107501042, max_lv=2)

    possible_entries = skill_data.get_all_possible_entries()

    # Bullet means Shikigami, no damage if Shikigami does not exist (expected)
    expected_max_total_mods = {
        ConditionComposite([Condition.BULLETS_SUMMONED_0, Condition.SELF_SEIMEI_SHIKIGAMI_LV_1]): 0,
        ConditionComposite([Condition.BULLETS_SUMMONED_1, Condition.SELF_SEIMEI_SHIKIGAMI_LV_1]): 15,
        ConditionComposite([Condition.BULLETS_SUMMONED_0, Condition.SELF_SEIMEI_SHIKIGAMI_LV_2]): 0,
        ConditionComposite([Condition.BULLETS_SUMMONED_1, Condition.SELF_SEIMEI_SHIKIGAMI_LV_2]): 25,
    }

    expected = set(expected_max_total_mods.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        assert \
            entry.total_mod_at_max == pytest.approx(expected_max_total_mods[entry.condition_comp]), \
            entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_seimei_s2(transformer_skill: SkillTransformer):
    # Seimei
    # https://dragalialost.wiki/w/Seimei
    skill_data_base = transformer_skill.transform_attacking(107501042)

    # For some reason, they inserted dummy data yet again (Lv 3)

    # Shikigami Level 1
    skill_data = skill_data_base.with_conditions(ConditionComposite(
        [Condition.BULLETS_SUMMONED_1, Condition.SELF_SEIMEI_SHIKIGAMI_LV_1]
    ))

    assert skill_data.hit_count == [1, 1, 0]
    assert skill_data.hit_count_at_max == 0
    assert skill_data.total_mod == pytest.approx([13.5, 15, 0])
    assert skill_data.total_mod_at_max == pytest.approx(0)
    assert skill_data.mods == [[13.5], [15], []]
    assert skill_data.mods_at_max == []
    assert skill_data.max_level == 3

    # Shikigami Level 2
    skill_data = skill_data_base.with_conditions(ConditionComposite(
        [Condition.BULLETS_SUMMONED_1, Condition.SELF_SEIMEI_SHIKIGAMI_LV_2]
    ))

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([22.5, 25, 25])
    assert skill_data.total_mod_at_max == pytest.approx(25)
    assert skill_data.mods == [[22.5], [25], [25]]
    assert skill_data.mods_at_max == [25]
    assert skill_data.max_level == 3


def test_seimei_ss(transformer_skill: SkillTransformer):
    # Seimei
    # https://dragalialost.wiki/w/Seimei
    skill_data_base = transformer_skill.transform_attacking(107501043)

    skill_data = skill_data_base.with_conditions()

    # For some reason, they inserted dummy data yet again (Lv 3)

    assert skill_data.hit_count == [1, 1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([22.5, 25, 25])
    assert skill_data.total_mod_at_max == pytest.approx(25)
    assert skill_data.mods == [[22.5], [25], [25]]
    assert skill_data.mods_at_max == [25]
    assert skill_data.max_level == 3
