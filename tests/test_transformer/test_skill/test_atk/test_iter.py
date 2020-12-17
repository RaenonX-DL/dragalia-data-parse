from itertools import product

import pytest

from dlparse.enums import SkillCondition, SkillConditionCategories, SkillConditionComposite
from dlparse.model import BuffCountBoostData
from dlparse.transformer import SkillTransformer


def test_no_condition(transformer_skill: SkillTransformer):
    # Cibella S2
    # https://dragalialost.gamepedia.com/Cibella
    skill_data = transformer_skill.transform_attacking(105302012)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(): 14.45 * 2,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp], entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_has_crisis_and_punisher_1(transformer_skill: SkillTransformer):
    # Veronica S1
    # https://dragalialost.gamepedia.com/Veronica

    # Exporting
    skill_data = transformer_skill.transform_attacking(107505011, is_exporting=True)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(): 24.77,
        SkillConditionComposite(SkillCondition.TARGET_POISONED): 29.724,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        expected_total_mod = expected_max_total_mods[entry.condition_comp]

        assert entry.total_mod_at_max == pytest.approx(expected_total_mod), entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"

    # Not exporting
    skill_data = transformer_skill.transform_attacking(107505011, is_exporting=False)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(SkillCondition.SELF_HP_FULL): 24.77,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_70): 25.88465,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_50): 27.86625,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_30): 30.83865,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_20): 32.6964,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_10): 34.80185,
        SkillConditionComposite(SkillCondition.SELF_HP_1): 37.155,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_FULL]): 29.724,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_EQ_70]): 31.06158,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_EQ_50]): 33.4395,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_EQ_30]): 37.00638,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_EQ_20]): 39.23568,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_EQ_10]): 41.76222,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_1]): 44.586,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        expected_total_mod = expected_max_total_mods[entry.condition_comp]

        assert entry.total_mod_at_max == pytest.approx(expected_total_mod), entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_has_crisis_and_punisher_2(transformer_skill: SkillTransformer):
    # Louise S2
    # https://dragalialost.gamepedia.com/Louise

    # Exporting
    skill_data = transformer_skill.transform_attacking(106503012, is_exporting=True)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(): 20.94,
        SkillConditionComposite(SkillCondition.TARGET_POISONED): 31.41,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == pytest.approx(expected_max_total_mods[entry.condition_comp]), \
            entry.condition_comp

        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"

    # Not exporting
    skill_data = transformer_skill.transform_attacking(106503012, is_exporting=False)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(SkillCondition.SELF_HP_FULL): 20.94,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_70): 19.9977,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_50): 18.3225,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_30): 15.8097,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_20): 14.2392,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_10): 12.4593,
        SkillConditionComposite(SkillCondition.SELF_HP_1): 10.47,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_FULL]): 31.41,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_EQ_70]): 29.99655,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_EQ_50]): 27.48375,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_EQ_30]): 23.71455,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_EQ_20]): 21.3588,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_EQ_10]): 18.68895,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_1]): 15.705,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == pytest.approx(expected_max_total_mods[entry.condition_comp]), \
            entry.condition_comp

        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_punisher_only(transformer_skill: SkillTransformer):
    # Lathna S2
    # https://dragalialost.gamepedia.com/Lathna
    skill_data = transformer_skill.transform_attacking(105505022)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(): 17.26,
        SkillConditionComposite(SkillCondition.TARGET_POISONED): 34.52,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp]
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_crisis_only(transformer_skill: SkillTransformer):
    # Bellina S2
    # https://dragalialost.gamepedia.com/Bellina

    # Exporting
    skill_data = transformer_skill.transform_attacking(103505034, is_exporting=True)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(): 12.12,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp], entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"

    # Not exporting
    skill_data = transformer_skill.transform_attacking(103505034, is_exporting=False)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(SkillCondition.SELF_HP_FULL): 12.12,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_70): 14.3016,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_50): 18.18,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_30): 23.9976,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_20): 27.6336,
        SkillConditionComposite(SkillCondition.SELF_HP_EQ_10): 31.7544,
        SkillConditionComposite(SkillCondition.SELF_HP_1): 36.36,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp], entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_buff_count_direct(transformer_skill: SkillTransformer):
    # For indirect buff boost tests, refer to each character instead (such as Lapis)

    # Karina S1
    # https://dragalialost.gamepedia.com/Karina

    # Not exporting
    skill_data = transformer_skill.transform_attacking(104402011, is_exporting=False)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(SkillCondition.SELF_BUFF_0): 16.36 * (1 + 0.05 * 0),
        SkillConditionComposite(SkillCondition.SELF_BUFF_1): 16.36 * (1 + 0.05 * 1),
        SkillConditionComposite(SkillCondition.SELF_BUFF_2): 16.36 * (1 + 0.05 * 2),
        SkillConditionComposite(SkillCondition.SELF_BUFF_3): 16.36 * (1 + 0.05 * 3),
        SkillConditionComposite(SkillCondition.SELF_BUFF_4): 16.36 * (1 + 0.05 * 4),
        SkillConditionComposite(SkillCondition.SELF_BUFF_5): 16.36 * (1 + 0.05 * 5),
        SkillConditionComposite(SkillCondition.SELF_BUFF_6): 16.36 * (1 + 0.05 * 6),
        SkillConditionComposite(SkillCondition.SELF_BUFF_7): 16.36 * (1 + 0.05 * 7),
        SkillConditionComposite(SkillCondition.SELF_BUFF_8): 16.36 * (1 + 0.05 * 8),
        SkillConditionComposite(SkillCondition.SELF_BUFF_9): 16.36 * (1 + 0.05 * 9),
        SkillConditionComposite(SkillCondition.SELF_BUFF_10): 16.36 * (1 + 0.05 * 10),
        SkillConditionComposite(SkillCondition.SELF_BUFF_15): 16.36 * (1 + 0.05 * 15),
        SkillConditionComposite(SkillCondition.SELF_BUFF_20): 16.36 * (1 + 0.05 * 20),
        SkillConditionComposite(SkillCondition.SELF_BUFF_25): 16.36 * (1 + 0.05 * 25),
        SkillConditionComposite(SkillCondition.SELF_BUFF_30): 16.36 * (1 + 0.05 * 30),
        SkillConditionComposite(SkillCondition.SELF_BUFF_35): 16.36 * (1 + 0.05 * 35),
        SkillConditionComposite(SkillCondition.SELF_BUFF_40): 16.36 * (1 + 0.05 * 40),
        SkillConditionComposite(SkillCondition.SELF_BUFF_45): 16.36 * (1 + 0.05 * 45),
        SkillConditionComposite(SkillCondition.SELF_BUFF_50): 16.36 * (1 + 0.05 * 50),
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp], entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"

    # Exporting
    skill_data = transformer_skill.transform_attacking(104402011, is_exporting=True)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(): 16.36
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp], entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_buff_count_data(transformer_skill: SkillTransformer):
    # Lapis S2
    # https://dragalialost.gamepedia.com/Lapis

    # Not exporting
    skill_data = transformer_skill.transform_attacking(109502012, is_exporting=False)

    possible_entries = skill_data.get_all_possible_entries()

    expected_buff_count_conds = [
        SkillCondition.SELF_BUFF_0,
        SkillCondition.SELF_BUFF_1,
        SkillCondition.SELF_BUFF_2,
        SkillCondition.SELF_BUFF_3,
        SkillCondition.SELF_BUFF_4,
        SkillCondition.SELF_BUFF_5,
        SkillCondition.SELF_BUFF_6,
        SkillCondition.SELF_BUFF_7,
        SkillCondition.SELF_BUFF_8,
        SkillCondition.SELF_BUFF_9,
        SkillCondition.SELF_BUFF_10,
        SkillCondition.SELF_BUFF_15,
        SkillCondition.SELF_BUFF_20,
        SkillCondition.SELF_BUFF_25,
        SkillCondition.SELF_BUFF_30,
        SkillCondition.SELF_BUFF_35,
        SkillCondition.SELF_BUFF_40,
        SkillCondition.SELF_BUFF_45,
        SkillCondition.SELF_BUFF_50,
    ]
    expected_addl_conds = [
        SkillCondition.SELF_LAPIS_CARD_0,
        SkillCondition.SELF_LAPIS_CARD_1,
        SkillCondition.SELF_LAPIS_CARD_2,
        SkillCondition.SELF_LAPIS_CARD_3,
    ]
    expected_in_effect_rates = {
        SkillConditionComposite([buff_count_cond, addl_cond]):
            min(
                SkillConditionCategories.self_buff_count.convert(buff_count_cond) * 0.05
                + SkillConditionCategories.self_lapis_card.convert(addl_cond) * 0.2,
                0.8
            )
        for buff_count_cond, addl_cond in product(expected_buff_count_conds, expected_addl_conds)
    }
    expected_max_total_mods = {cond: 15.05 * 2 * (1 + up_rate) for cond, up_rate in expected_in_effect_rates.items()}

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    lapis_cat = SkillConditionCategories.self_lapis_card

    for entry in possible_entries:
        expected_in_effect_rate = expected_in_effect_rates[entry.condition_comp]
        expected_total_mods = expected_max_total_mods[entry.condition_comp]

        boost_data = BuffCountBoostData(
            expected_in_effect_rate, 0.8, 0.05,
            1319, 3 - lapis_cat.convert(lapis_cat.extract(entry.condition_comp)), 0.2
        )

        assert entry.total_mod_at_max == pytest.approx(expected_total_mods), entry.condition_comp
        assert entry.buff_count_boost_mtx[-1] == [boost_data] * 2, entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"

    # Exporting
    skill_data = transformer_skill.transform_attacking(109502012, is_exporting=True)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_0): 30.10,
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_1): 36.12,
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_2): 42.14,
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_3): 48.16,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        expected_total_mods = expected_max_total_mods[entry.condition_comp]

        assert entry.total_mod_at_max == pytest.approx(expected_total_mods), entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_buff_count_bonus_bullet(transformer_skill: SkillTransformer):
    # Summer Cleo S1
    # https://dragalialost.gamepedia.com/Summer_Cleo
    skill_data = transformer_skill.transform_attacking(106504011)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(SkillCondition.SELF_BUFF_0): 1.07 * 3 + 5.4 + 1.07 * 0,
        SkillConditionComposite(SkillCondition.SELF_BUFF_1): 1.07 * 3 + 5.4 + 1.07 * 1,
        SkillConditionComposite(SkillCondition.SELF_BUFF_2): 1.07 * 3 + 5.4 + 1.07 * 2,
        SkillConditionComposite(SkillCondition.SELF_BUFF_3): 1.07 * 3 + 5.4 + 1.07 * 3,
        SkillConditionComposite(SkillCondition.SELF_BUFF_4): 1.07 * 3 + 5.4 + 1.07 * 4,
        SkillConditionComposite(SkillCondition.SELF_BUFF_5): 1.07 * 3 + 5.4 + 1.07 * 5,
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.SELF_BUFF_0]):
            (1.07 * 3 + 5.4 + 1.07 * 0) * 1.1,
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.SELF_BUFF_1]):
            (1.07 * 3 + 5.4 + 1.07 * 1) * 1.1,
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.SELF_BUFF_2]):
            (1.07 * 3 + 5.4 + 1.07 * 2) * 1.1,
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.SELF_BUFF_3]):
            (1.07 * 3 + 5.4 + 1.07 * 3) * 1.1,
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.SELF_BUFF_4]):
            (1.07 * 3 + 5.4 + 1.07 * 4) * 1.1,
        SkillConditionComposite([SkillCondition.TARGET_PARALYZED, SkillCondition.SELF_BUFF_5]):
            (1.07 * 3 + 5.4 + 1.07 * 5) * 1.1,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == pytest.approx(expected_max_total_mods[entry.condition_comp]), \
            entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_partial_attacking(transformer_skill: SkillTransformer):
    # Elisanne S1
    # https://dragalialost.gamepedia.com/Elisanne
    skill_data = transformer_skill.transform_attacking(105402011)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(): 1.5 * 5,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        # noinspection PyTypeChecker
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp], entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"
