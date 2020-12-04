import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
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
    skill_data = transformer_skill.transform_attacking(107505011)

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
    skill_data = transformer_skill.transform_attacking(106503012)

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
    skill_data = transformer_skill.transform_attacking(103505034)

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


def test_buff_count_only(transformer_skill: SkillTransformer):
    # Karina S1
    # https://dragalialost.gamepedia.com/Karina
    skill_data = transformer_skill.transform_attacking(104402011)

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
