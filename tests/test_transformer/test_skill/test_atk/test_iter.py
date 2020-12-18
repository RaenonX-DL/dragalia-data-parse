from itertools import product

import pytest

from dlparse.enums import Condition, ConditionCategories, ConditionComposite
from dlparse.model import BuffCountBoostData
from dlparse.transformer import SkillTransformer


def test_no_condition(transformer_skill: SkillTransformer):
    # Cibella S2
    # https://dragalialost.gamepedia.com/Cibella
    skill_data = transformer_skill.transform_attacking(105302012)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        ConditionComposite(): 14.45 * 2,
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
        ConditionComposite(): 24.77,
        ConditionComposite(Condition.TARGET_POISONED): 29.724,
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
        ConditionComposite(Condition.SELF_HP_FULL): 24.77,
        ConditionComposite(Condition.SELF_HP_EQ_70): 25.88465,
        ConditionComposite(Condition.SELF_HP_EQ_50): 27.86625,
        ConditionComposite(Condition.SELF_HP_EQ_30): 30.83865,
        ConditionComposite(Condition.SELF_HP_EQ_20): 32.6964,
        ConditionComposite(Condition.SELF_HP_EQ_10): 34.80185,
        ConditionComposite(Condition.SELF_HP_1): 37.155,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_FULL]): 29.724,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_EQ_70]): 31.06158,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_EQ_50]): 33.4395,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_EQ_30]): 37.00638,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_EQ_20]): 39.23568,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_EQ_10]): 41.76222,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_1]): 44.586,
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
        ConditionComposite(): 20.94,
        ConditionComposite(Condition.TARGET_POISONED): 31.41,
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
        ConditionComposite(Condition.SELF_HP_FULL): 20.94,
        ConditionComposite(Condition.SELF_HP_EQ_70): 19.9977,
        ConditionComposite(Condition.SELF_HP_EQ_50): 18.3225,
        ConditionComposite(Condition.SELF_HP_EQ_30): 15.8097,
        ConditionComposite(Condition.SELF_HP_EQ_20): 14.2392,
        ConditionComposite(Condition.SELF_HP_EQ_10): 12.4593,
        ConditionComposite(Condition.SELF_HP_1): 10.47,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_FULL]): 31.41,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_EQ_70]): 29.99655,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_EQ_50]): 27.48375,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_EQ_30]): 23.71455,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_EQ_20]): 21.3588,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_EQ_10]): 18.68895,
        ConditionComposite([Condition.TARGET_POISONED, Condition.SELF_HP_1]): 15.705,
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
        ConditionComposite(): 17.26,
        ConditionComposite(Condition.TARGET_POISONED): 34.52,
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
        ConditionComposite(): 12.12,
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
        ConditionComposite(Condition.SELF_HP_FULL): 12.12,
        ConditionComposite(Condition.SELF_HP_EQ_70): 14.3016,
        ConditionComposite(Condition.SELF_HP_EQ_50): 18.18,
        ConditionComposite(Condition.SELF_HP_EQ_30): 23.9976,
        ConditionComposite(Condition.SELF_HP_EQ_20): 27.6336,
        ConditionComposite(Condition.SELF_HP_EQ_10): 31.7544,
        ConditionComposite(Condition.SELF_HP_1): 36.36,
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
        ConditionComposite(Condition.SELF_BUFF_0): 16.36 * (1 + 0.05 * 0),
        ConditionComposite(Condition.SELF_BUFF_1): 16.36 * (1 + 0.05 * 1),
        ConditionComposite(Condition.SELF_BUFF_2): 16.36 * (1 + 0.05 * 2),
        ConditionComposite(Condition.SELF_BUFF_3): 16.36 * (1 + 0.05 * 3),
        ConditionComposite(Condition.SELF_BUFF_4): 16.36 * (1 + 0.05 * 4),
        ConditionComposite(Condition.SELF_BUFF_5): 16.36 * (1 + 0.05 * 5),
        ConditionComposite(Condition.SELF_BUFF_6): 16.36 * (1 + 0.05 * 6),
        ConditionComposite(Condition.SELF_BUFF_7): 16.36 * (1 + 0.05 * 7),
        ConditionComposite(Condition.SELF_BUFF_8): 16.36 * (1 + 0.05 * 8),
        ConditionComposite(Condition.SELF_BUFF_9): 16.36 * (1 + 0.05 * 9),
        ConditionComposite(Condition.SELF_BUFF_10): 16.36 * (1 + 0.05 * 10),
        ConditionComposite(Condition.SELF_BUFF_15): 16.36 * (1 + 0.05 * 15),
        ConditionComposite(Condition.SELF_BUFF_20): 16.36 * (1 + 0.05 * 20),
        ConditionComposite(Condition.SELF_BUFF_25): 16.36 * (1 + 0.05 * 25),
        ConditionComposite(Condition.SELF_BUFF_30): 16.36 * (1 + 0.05 * 30),
        ConditionComposite(Condition.SELF_BUFF_35): 16.36 * (1 + 0.05 * 35),
        ConditionComposite(Condition.SELF_BUFF_40): 16.36 * (1 + 0.05 * 40),
        ConditionComposite(Condition.SELF_BUFF_45): 16.36 * (1 + 0.05 * 45),
        ConditionComposite(Condition.SELF_BUFF_50): 16.36 * (1 + 0.05 * 50),
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
        ConditionComposite(): 16.36
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
        Condition.SELF_BUFF_0,
        Condition.SELF_BUFF_1,
        Condition.SELF_BUFF_2,
        Condition.SELF_BUFF_3,
        Condition.SELF_BUFF_4,
        Condition.SELF_BUFF_5,
        Condition.SELF_BUFF_6,
        Condition.SELF_BUFF_7,
        Condition.SELF_BUFF_8,
        Condition.SELF_BUFF_9,
        Condition.SELF_BUFF_10,
        Condition.SELF_BUFF_15,
        Condition.SELF_BUFF_20,
        Condition.SELF_BUFF_25,
        Condition.SELF_BUFF_30,
        Condition.SELF_BUFF_35,
        Condition.SELF_BUFF_40,
        Condition.SELF_BUFF_45,
        Condition.SELF_BUFF_50,
    ]
    expected_addl_conds = [
        Condition.SELF_LAPIS_CARD_0,
        Condition.SELF_LAPIS_CARD_1,
        Condition.SELF_LAPIS_CARD_2,
        Condition.SELF_LAPIS_CARD_3,
    ]
    expected_in_effect_rates = {
        ConditionComposite([buff_count_cond, addl_cond]):
            min(
                ConditionCategories.self_buff_count.convert(buff_count_cond) * 0.05
                + ConditionCategories.self_lapis_card.convert(addl_cond) * 0.2,
                0.8
            )
        for buff_count_cond, addl_cond in product(expected_buff_count_conds, expected_addl_conds)
    }
    expected_max_total_mods = {cond: 15.05 * 2 * (1 + up_rate) for cond, up_rate in expected_in_effect_rates.items()}

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    lapis_cat = ConditionCategories.self_lapis_card

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
        ConditionComposite(Condition.SELF_LAPIS_CARD_0): 30.10,
        ConditionComposite(Condition.SELF_LAPIS_CARD_1): 36.12,
        ConditionComposite(Condition.SELF_LAPIS_CARD_2): 42.14,
        ConditionComposite(Condition.SELF_LAPIS_CARD_3): 48.16,
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
        ConditionComposite(Condition.SELF_BUFF_0): 1.07 * 3 + 5.4 + 1.07 * 0,
        ConditionComposite(Condition.SELF_BUFF_1): 1.07 * 3 + 5.4 + 1.07 * 1,
        ConditionComposite(Condition.SELF_BUFF_2): 1.07 * 3 + 5.4 + 1.07 * 2,
        ConditionComposite(Condition.SELF_BUFF_3): 1.07 * 3 + 5.4 + 1.07 * 3,
        ConditionComposite(Condition.SELF_BUFF_4): 1.07 * 3 + 5.4 + 1.07 * 4,
        ConditionComposite(Condition.SELF_BUFF_5): 1.07 * 3 + 5.4 + 1.07 * 5,
        ConditionComposite([Condition.TARGET_PARALYZED, Condition.SELF_BUFF_0]):
            (1.07 * 3 + 5.4 + 1.07 * 0) * 1.1,
        ConditionComposite([Condition.TARGET_PARALYZED, Condition.SELF_BUFF_1]):
            (1.07 * 3 + 5.4 + 1.07 * 1) * 1.1,
        ConditionComposite([Condition.TARGET_PARALYZED, Condition.SELF_BUFF_2]):
            (1.07 * 3 + 5.4 + 1.07 * 2) * 1.1,
        ConditionComposite([Condition.TARGET_PARALYZED, Condition.SELF_BUFF_3]):
            (1.07 * 3 + 5.4 + 1.07 * 3) * 1.1,
        ConditionComposite([Condition.TARGET_PARALYZED, Condition.SELF_BUFF_4]):
            (1.07 * 3 + 5.4 + 1.07 * 4) * 1.1,
        ConditionComposite([Condition.TARGET_PARALYZED, Condition.SELF_BUFF_5]):
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
        ConditionComposite(): 1.5 * 5,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        # noinspection PyTypeChecker
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp], entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"
