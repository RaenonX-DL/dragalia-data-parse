import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer


def test_catherine(transformer_skill: SkillTransformer):
    skill_id_mods = {
        105502042: 0.54 * 46,
        105502043: 0.54 * 58,
        105502044: 0.54 * 66,
        105502045: 0.54 * 37 + 1.22 * 37,
        105502046: 0.54 * 46
    }

    for skill_id, total_mod in skill_id_mods.items():
        skill_data = transformer_skill.transform_attacking(skill_id)

        possible_entries = skill_data.get_all_possible_entries()

        expected_max_total_mods = {
            SkillConditionComposite(): total_mod,
        }

        expected = set(expected_max_total_mods.keys())
        actual = {entry.condition_comp for entry in possible_entries}

        assert expected == actual, actual.symmetric_difference(expected)

        for entry in possible_entries:
            assert entry.total_mod_at_max == pytest.approx(expected_max_total_mods[entry.condition_comp])


def test_yukata_curran(transformer_skill: SkillTransformer):
    # Yukata Curran S1 - Unmasked
    # https://dragalialost.gamepedia.com/Yukata_Curran
    skill_data = transformer_skill.transform_attacking(103504041)

    possible_entries = skill_data.get_all_possible_entries()

    lv_3_single_no_affliction = 1.65 * 3
    lv_3_single_paralyzed = 2.145 * 3

    dmg_ups = [
        sum(0.55 ** deterioration_count for deterioration_count in range(1)),
        sum(0.55 ** deterioration_count for deterioration_count in range(2)),
        sum(0.55 ** deterioration_count for deterioration_count in range(3)),
        sum(0.55 ** deterioration_count for deterioration_count in range(4)),
        sum(0.55 ** deterioration_count for deterioration_count in range(5)),
        sum(0.55 ** deterioration_count for deterioration_count in range(6)),
    ]

    expected_max_total_mods = {
        SkillConditionComposite(SkillCondition.BULLET_HIT_1): pytest.approx(lv_3_single_no_affliction * dmg_ups[0]),
        SkillConditionComposite(SkillCondition.BULLET_HIT_2): pytest.approx(lv_3_single_no_affliction * dmg_ups[1]),
        SkillConditionComposite(SkillCondition.BULLET_HIT_3): pytest.approx(lv_3_single_no_affliction * dmg_ups[2]),
        SkillConditionComposite(SkillCondition.BULLET_HIT_4): pytest.approx(lv_3_single_no_affliction * dmg_ups[3]),
        SkillConditionComposite(SkillCondition.BULLET_HIT_5): pytest.approx(lv_3_single_no_affliction * dmg_ups[4]),
        SkillConditionComposite(SkillCondition.BULLET_HIT_6): pytest.approx(lv_3_single_no_affliction * dmg_ups[5]),
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.BULLET_HIT_1]):
            pytest.approx(lv_3_single_paralyzed * dmg_ups[0]),
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.BULLET_HIT_2]):
            pytest.approx(lv_3_single_paralyzed * dmg_ups[1]),
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.BULLET_HIT_3]):
            pytest.approx(lv_3_single_paralyzed * dmg_ups[2]),
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.BULLET_HIT_4]):
            pytest.approx(lv_3_single_paralyzed * dmg_ups[3]),
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.BULLET_HIT_5]):
            pytest.approx(lv_3_single_paralyzed * dmg_ups[4]),
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.BULLET_HIT_6]):
            pytest.approx(lv_3_single_paralyzed * dmg_ups[5]),
    }

    expected = set(expected_max_total_mods.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp]
