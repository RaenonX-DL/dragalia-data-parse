from dlparse.enums import SkillCondition
from dlparse.transformer import SkillTransformer


def test_has_crisis_and_punisher(transformer_skill: SkillTransformer):
    # Louise S2
    # https://dragalialost.gamepedia.com/Louise
    skill_data = transformer_skill.transform_attacking(106503012)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        (SkillCondition.SELF_HP_FULL,): 6.98 * 3,
        (SkillCondition.SELF_HP_1,): 3.49 * 3,
        (SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_FULL): 10.47 * 3,
        (SkillCondition.TARGET_POISONED, SkillCondition.SELF_HP_1): 5.235 * 3,
    }

    assert set(expected_max_total_mods.keys()) == {entry.conditions for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.conditions], entry.conditions


def test_punisher_only(transformer_skill: SkillTransformer):
    # Lathna S2
    # https://dragalialost.gamepedia.com/Lathna
    skill_data = transformer_skill.transform_attacking(105505022)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        (): 17.26,
        (SkillCondition.TARGET_POISONED,): 34.52,
    }

    assert set(expected_max_total_mods.keys()) == {entry.conditions for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.conditions]


def test_crisis_only(transformer_skill: SkillTransformer):
    # Bellina S2
    # https://dragalialost.gamepedia.com/Bellina
    skill_data = transformer_skill.transform_attacking(103505034)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        (SkillCondition.SELF_HP_1,): 36.36,
        (SkillCondition.SELF_HP_FULL,): 12.12,
    }

    assert set(expected_max_total_mods.keys()) == {entry.conditions for entry in possible_entries}

    for entry in possible_entries:
        assert entry.total_mod_at_max == expected_max_total_mods[entry.conditions], entry.conditions


def test_no_condition(transformer_skill: SkillTransformer):
    # Cibella S2
    # https://dragalialost.gamepedia.com/Cibella
    skill_data = transformer_skill.transform_attacking(105302012)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        (): 14.45 * 2,
    }

    assert set(expected_max_total_mods.keys()) == {entry.conditions for entry in possible_entries}

    for entry in possible_entries:
        # noinspection PyTypeChecker
        assert entry.total_mod_at_max == expected_max_total_mods[entry.conditions], entry.conditions


def test_partial_attacking(transformer_skill: SkillTransformer):
    # Elisanne S1
    # https://dragalialost.gamepedia.com/Elisanne

    skill_data = transformer_skill.transform_attacking(105402011)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        (): 1.5 * 5,
    }

    assert set(expected_max_total_mods.keys()) == {entry.conditions for entry in possible_entries}

    for entry in possible_entries:
        # noinspection PyTypeChecker
        assert entry.total_mod_at_max == expected_max_total_mods[entry.conditions], entry.conditions
