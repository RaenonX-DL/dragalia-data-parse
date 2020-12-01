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


def test_has_crisis_and_punisher(transformer_skill: SkillTransformer):
    # Louise S2
    # https://dragalialost.gamepedia.com/Louise
    skill_data = transformer_skill.transform_attacking(106503012)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(SkillCondition.SELF_HP_FULL): 6.98 * 3,
        SkillConditionComposite(SkillCondition.SELF_HP_1): 3.49 * 3,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_FULL]): 10.47 * 3,
        SkillConditionComposite([SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_1]): 5.235 * 3,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.condition_comp], entry.condition_comp
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
        SkillConditionComposite(SkillCondition.SELF_HP_1): 36.36,
        SkillConditionComposite(SkillCondition.SELF_HP_FULL): 12.12,
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
