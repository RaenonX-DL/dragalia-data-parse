from itertools import product

import pytest

from dlparse.enums import SkillCondition, SkillConditionCategories, SkillConditionComposite
from dlparse.model import BuffCountBoostData
from dlparse.transformer import SkillTransformer


def test_uncapped_get_all_with_sectioned(transformer_skill: SkillTransformer):
    # Karina S1
    # https://dragalialost.gamepedia.com/Karina
    skill_data = transformer_skill.transform_attacking(104402011, with_sectioned_buffs=True)

    possible_entries = skill_data.get_all_possible_entries()

    expected_max_total_mods = {
        SkillConditionComposite(SkillCondition.SELF_BUFF_0, ): 16.36 * (1 + 0.05 * 0),
        SkillConditionComposite(SkillCondition.SELF_BUFF_1, ): 16.36 * (1 + 0.05 * 1),
        SkillConditionComposite(SkillCondition.SELF_BUFF_2, ): 16.36 * (1 + 0.05 * 2),
        SkillConditionComposite(SkillCondition.SELF_BUFF_3, ): 16.36 * (1 + 0.05 * 3),
        SkillConditionComposite(SkillCondition.SELF_BUFF_4, ): 16.36 * (1 + 0.05 * 4),
        SkillConditionComposite(SkillCondition.SELF_BUFF_5, ): 16.36 * (1 + 0.05 * 5),
        SkillConditionComposite(SkillCondition.SELF_BUFF_6, ): 16.36 * (1 + 0.05 * 6),
        SkillConditionComposite(SkillCondition.SELF_BUFF_7, ): 16.36 * (1 + 0.05 * 7),
        SkillConditionComposite(SkillCondition.SELF_BUFF_8, ): 16.36 * (1 + 0.05 * 8),
        SkillConditionComposite(SkillCondition.SELF_BUFF_9, ): 16.36 * (1 + 0.05 * 9),
        SkillConditionComposite(SkillCondition.SELF_BUFF_10, ): 16.36 * (1 + 0.05 * 10),
        SkillConditionComposite(SkillCondition.SELF_BUFF_15, ): 16.36 * (1 + 0.05 * 15),
        SkillConditionComposite(SkillCondition.SELF_BUFF_20, ): 16.36 * (1 + 0.05 * 20),
        SkillConditionComposite(SkillCondition.SELF_BUFF_25, ): 16.36 * (1 + 0.05 * 25),
        SkillConditionComposite(SkillCondition.SELF_BUFF_30, ): 16.36 * (1 + 0.05 * 30),
        SkillConditionComposite(SkillCondition.SELF_BUFF_35, ): 16.36 * (1 + 0.05 * 35),
        SkillConditionComposite(SkillCondition.SELF_BUFF_40, ): 16.36 * (1 + 0.05 * 40),
        SkillConditionComposite(SkillCondition.SELF_BUFF_45, ): 16.36 * (1 + 0.05 * 45),
        SkillConditionComposite(SkillCondition.SELF_BUFF_50, ): 16.36 * (1 + 0.05 * 50),
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        expected_total_mods = expected_max_total_mods[entry.condition_comp]
        expected_buff_boost_data = BuffCountBoostData(
            entry.condition_comp.buff_count_converted * 0.05, 0, 0.05,
            0, 0, 0
        )

        assert entry.total_mod_at_max == pytest.approx(expected_total_mods), entry.condition_comp
        assert entry.buff_boost_data_mtx[-1] == [expected_buff_boost_data] * 2
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_uncapped_get_all_without_sectioned(transformer_skill: SkillTransformer):
    # Karina S1
    # https://dragalialost.gamepedia.com/Karina
    skill_data = transformer_skill.transform_attacking(104402011, with_sectioned_buffs=False)

    possible_entries = skill_data.get_all_possible_entries()

    expected_buff_boost_data = BuffCountBoostData(0, 0, 0.05, 0, 0, 0)
    expected_max_total_mods = {
        SkillConditionComposite(): 16.36,
    }

    assert set(expected_max_total_mods.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        expected_total_mods = expected_max_total_mods[entry.condition_comp]

        assert entry.total_mod_at_max == pytest.approx(expected_total_mods), entry.condition_comp
        assert entry.buff_boost_data_mtx[-1] == [expected_buff_boost_data] * 2
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_capped_get_all_with_sectioned(transformer_skill: SkillTransformer):
    # Lapis S2
    # https://dragalialost.gamepedia.com/Lapis
    skill_data = transformer_skill.transform_attacking(109502012, with_sectioned_buffs=True)

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
        assert entry.buff_boost_data_mtx[-1] == [boost_data] * 2, entry.condition_comp
        del expected_max_total_mods[entry.condition_comp]

    assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_capped_get_all_without_sectioned(transformer_skill: SkillTransformer):
    # Lapis S2
    # https://dragalialost.gamepedia.com/Lapis
    skill_data = transformer_skill.transform_attacking(109502012, with_sectioned_buffs=False)

    possible_entries = skill_data.get_all_possible_entries()

    expected_data = {
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_0):
            (30.10, BuffCountBoostData(0, 0.8, 0.05, 1319, 3, 0.2)),
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_1):
            (36.12, BuffCountBoostData(0.2, 0.8, 0.05, 1319, 2, 0.2)),
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_2):
            (42.14, BuffCountBoostData(0.4, 0.8, 0.05, 1319, 1, 0.2)),
        SkillConditionComposite(SkillCondition.SELF_LAPIS_CARD_3):
            (48.16, BuffCountBoostData(0.6, 0.8, 0.05, 1319, 0, 0.2)),
    }

    assert set(expected_data.keys()) == {entry.condition_comp for entry in possible_entries}

    for entry in possible_entries:
        expected_total_mods, expected_boost_data = expected_data[entry.condition_comp]

        assert entry.total_mod_at_max == pytest.approx(expected_total_mods), entry.condition_comp
        assert entry.buff_boost_data_mtx[-1] == [expected_boost_data] * 2
        del expected_data[entry.condition_comp]

    assert len(expected_data) == 0, f"Conditions not tested: {set(expected_data.keys())}"
