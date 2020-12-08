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
            del expected_max_total_mods[entry.condition_comp]

        assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_yukata_curran_unmasked(transformer_skill: SkillTransformer):
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
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_nevin_s2_locked(transformer_skill: SkillTransformer):
    # Nevin S2 @ Sigil locked
    # https://dragalialost.gamepedia.com/Nevin
    skill_data = transformer_skill.transform_attacking(103505042)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(SkillCondition.SELF_SIGIL_RELEASED): 10,
        SkillConditionComposite(SkillCondition.SELF_SIGIL_LOCKED): 10,
    }

    expected = set(expected_max_total_mods.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp]
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_nevin_s2_released(transformer_skill: SkillTransformer):
    # Nevin S2 @ Sigil released
    # https://dragalialost.gamepedia.com/Nevin
    skill_data = transformer_skill.transform_attacking(103505044)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_0,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_0]): 0,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_0,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_1]): 1,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_0,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_2]): 2,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_0,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_3]): 3,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_1,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_0]): 3,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_1,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_1]): 4,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_1,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_2]): 5,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_1,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_3]): 6,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_2,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_0]): 6,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_2,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_1]): 7,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_2,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_2]): 8,
        SkillConditionComposite([SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_2,
                                 SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_3]): 9,
    }

    expected = set(expected_addl_at_max.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        expected_total = 10 + expected_addl_at_max[entry.condition_comp]

        assert pytest.approx(expected_total) == entry.total_mod_at_max, entry.condition_comp
        del expected_addl_at_max[entry.condition_comp]

    assert len(expected_addl_at_max) == 0, f"Conditions not tested: {set(expected_addl_at_max.keys())}"


def test_meene_s2(transformer_skill: SkillTransformer):
    # Meene S2
    # https://dragalialost.gamepedia.com/Meene
    skill_data = transformer_skill.transform_attacking(106503032)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        SkillConditionComposite([SkillCondition.BULLETS_ON_MAP_0]): 1.67 * 0,
        SkillConditionComposite([SkillCondition.BULLETS_ON_MAP_1]): 1.67 * 1,
        SkillConditionComposite([SkillCondition.BULLETS_ON_MAP_2]): 1.67 * 2,
        SkillConditionComposite([SkillCondition.BULLETS_ON_MAP_3]): 1.67 * 3,
        SkillConditionComposite([SkillCondition.BULLETS_ON_MAP_4]): 1.67 * 4,
        SkillConditionComposite([SkillCondition.BULLETS_ON_MAP_5]): 1.67 * 5,
        SkillConditionComposite([SkillCondition.BULLETS_ON_MAP_6]): 1.67 * 6,
        SkillConditionComposite([SkillCondition.BULLETS_ON_MAP_7]): 1.67 * 7,
        SkillConditionComposite([SkillCondition.BULLETS_ON_MAP_8]): 1.67 * 8,
        SkillConditionComposite([SkillCondition.BULLETS_ON_MAP_9]): 1.67 * 9,
    }

    expected = set(expected_addl_at_max.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert expected == actual, actual.symmetric_difference(expected)

    for entry in possible_entries:
        expected_total = 10 + expected_addl_at_max[entry.condition_comp]

        assert pytest.approx(expected_total) == entry.total_mod_at_max, entry.condition_comp
        del expected_addl_at_max[entry.condition_comp]

    assert len(expected_addl_at_max) == 0, f"Conditions not tested: {set(expected_addl_at_max.keys())}"


def test_ramona_s1(transformer_skill: SkillTransformer):
    # Ramona S1
    # https://dragalialost.gamepedia.com/Ramona
    skill_data = transformer_skill.transform_attacking(104501011)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        SkillConditionComposite([SkillCondition.ADDL_INPUT_0]): 3.76 + 2.93 * 3 + 2.93 * 0 + 3.76,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_1]): 3.76 + 2.93 * 3 + 2.93 * 1 + 3.76,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_2]): 3.76 + 2.93 * 3 + 2.93 * 2 + 3.76,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_3]): 3.76 + 2.93 * 3 + 2.93 * 3 + 3.76,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_4]): 3.76 + 2.93 * 3 + 2.93 * 4 + 3.76,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_5]): 3.76 + 2.93 * 3 + 2.93 * 5 + 3.76,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_6]): 3.76 + 2.93 * 3 + 2.93 * 6 + 3.76,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_0, SkillCondition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 0 + 4.888,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_1, SkillCondition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 1 + 4.888,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_2, SkillCondition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 2 + 4.888,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_3, SkillCondition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 3 + 4.888,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_4, SkillCondition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 4 + 4.888,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_5, SkillCondition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 5 + 4.888,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_6, SkillCondition.TARGET_BURNED]):
            4.888 + 3.809 * 3 + 3.809 * 6 + 4.888,
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


def test_lathna_s1(transformer_skill: SkillTransformer):
    # Lathna S1
    # https://dragalialost.gamepedia.com/Lathna
    skill_data = transformer_skill.transform_attacking(105505021)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        SkillConditionComposite([SkillCondition.ADDL_INPUT_0]): 2.61 * 3 + 2.61 * 0 + 2.61,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_1]): 2.61 * 3 + 2.61 * 1 + 2.61,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_2]): 2.61 * 3 + 2.61 * 2 + 2.61,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_3]): 2.61 * 3 + 2.61 * 3 + 2.61,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_4]): 2.61 * 4 + 2.61 * 3 + 2.61,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_0, SkillCondition.TARGET_POISONED]):
            5.22 * 3 + 5.22 * 0 + 5.22,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_1, SkillCondition.TARGET_POISONED]):
            5.22 * 3 + 5.22 * 1 + 5.22,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_2, SkillCondition.TARGET_POISONED]):
            5.22 * 3 + 5.22 * 2 + 5.22,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_3, SkillCondition.TARGET_POISONED]):
            5.22 * 3 + 5.22 * 3 + 5.22,
        SkillConditionComposite([SkillCondition.ADDL_INPUT_4, SkillCondition.TARGET_POISONED]):
            5.22 * 4 + 5.22 * 3 + 5.22,
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


def test_og_alex_s2(transformer_skill: SkillTransformer):
    # Original Alex S2
    # https://dragalialost.gamepedia.com/Alex
    skill_data = transformer_skill.transform_attacking(103405022)

    possible_entries = skill_data.get_all_possible_entries()

    # EXNOTE: Not yet 70 MC (2020/12/07), but S2 already have data for 3 levels (lv.3 does not have BK punisher)

    expected_addl_at_max = {
        SkillConditionComposite(): 2.01 * 3 + 4.02,
        SkillConditionComposite(SkillCondition.TARGET_BK_STATE): 2.01 * 3 + 4.02,
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
