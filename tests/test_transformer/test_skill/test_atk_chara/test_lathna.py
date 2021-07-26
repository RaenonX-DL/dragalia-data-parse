import pytest

from dlparse.enums import Condition, ConditionComposite
from dlparse.mono.manager import AssetManager
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries_s1(asset_manager: AssetManager, transformer_skill: SkillTransformer):
    # Lathna S1
    # https://dragalialost.wiki/w/Lathna
    ability_ids = asset_manager.asset_chara_data.get_data_by_id(10550502).ability_ids_all_level
    skill_data = transformer_skill.transform_attacking(105505021, ability_ids=ability_ids)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite([Condition.ADDL_INPUT_0]): 2.61 * 3 + 2.61 * 0,
        ConditionComposite([Condition.ADDL_INPUT_1]): 2.61 * 3 + 2.61 * 1,
        ConditionComposite([Condition.ADDL_INPUT_2]): 2.61 * 3 + 2.61 * 2,
        ConditionComposite([Condition.ADDL_INPUT_3]): 2.61 * 3 + 2.61 * 3,
        ConditionComposite([Condition.ADDL_INPUT_4]): 2.61 * 3 + 2.61 * 4,
        ConditionComposite([Condition.ADDL_INPUT_0, Condition.TARGET_POISONED]): 5.22 * 3 + 5.22 * 0,
        ConditionComposite([Condition.ADDL_INPUT_1, Condition.TARGET_POISONED]): 5.22 * 3 + 5.22 * 1,
        ConditionComposite([Condition.ADDL_INPUT_2, Condition.TARGET_POISONED]): 5.22 * 3 + 5.22 * 2,
        ConditionComposite([Condition.ADDL_INPUT_3, Condition.TARGET_POISONED]): 5.22 * 3 + 5.22 * 3,
        ConditionComposite([Condition.ADDL_INPUT_4, Condition.TARGET_POISONED]): 5.22 * 3 + 5.22 * 4,
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


def test_s1(asset_manager: AssetManager, transformer_skill: SkillTransformer):
    # Lathna S1
    # https://dragalialost.wiki/w/Lathna
    ability_ids = asset_manager.asset_chara_data.get_data_by_id(10550502).ability_ids_all_level
    skill_data_base = transformer_skill.transform_attacking(105505021, ability_ids=ability_ids)

    pre_dmg = [
        [1.79] * 3,
        [1.99] * 3,
        [2.21] * 3,
        [2.61] * 3,
    ]
    addl_hits = {
        ConditionComposite(Condition.ADDL_INPUT_0): 0,
        ConditionComposite(Condition.ADDL_INPUT_1): 1,
        ConditionComposite(Condition.ADDL_INPUT_2): 2,
        ConditionComposite(Condition.ADDL_INPUT_3): 3,
        ConditionComposite(Condition.ADDL_INPUT_4): 4,
    }
    post_dmg = [
        [],
        [],
        [],
        []
    ]

    for cond_comp, bonus_hits in addl_hits.items():
        skill_data = skill_data_base.with_conditions(cond_comp)

        assert skill_data.hit_count == [3 + bonus_hits, 3 + bonus_hits, 3 + bonus_hits, 3 + bonus_hits]
        assert skill_data.hit_count_at_max == 3 + bonus_hits
        assert skill_data.total_mod == pytest.approx([
            sum(pre_dmg[0]) + 1.79 * bonus_hits + sum(post_dmg[0]),
            sum(pre_dmg[1]) + 1.99 * bonus_hits + sum(post_dmg[1]),
            sum(pre_dmg[2]) + 2.21 * bonus_hits + sum(post_dmg[2]),
            sum(pre_dmg[3]) + 2.61 * bonus_hits + sum(post_dmg[3]),
        ])
        assert skill_data.total_mod_at_max == pytest.approx(sum(pre_dmg[3]) + 2.61 * bonus_hits + sum(post_dmg[3]))
        assert skill_data.mods == approx_matrix([
            pre_dmg[0] + [1.79] * bonus_hits + post_dmg[0],
            pre_dmg[1] + [1.99] * bonus_hits + post_dmg[1],
            pre_dmg[2] + [2.21] * bonus_hits + post_dmg[2],
            pre_dmg[3] + [2.61] * bonus_hits + post_dmg[3],
        ])
        assert skill_data.mods_at_max == pytest.approx(pre_dmg[3] + [2.61] * bonus_hits + post_dmg[3])
        assert skill_data.max_level == 4


def test_iter_entries_unique_dragon_ult(asset_manager: AssetManager, transformer_skill: SkillTransformer):
    # Lathna Unique Dragon Ult
    # https://dragalialost.wiki/w/Nyarlathotep_(Lathna)
    ability_ids = asset_manager.asset_chara_data.get_data_by_id(10550502).ability_ids_all_level
    skill_data = transformer_skill.transform_attacking(299000041, ability_ids=ability_ids)

    possible_entries = skill_data.get_all_possible_entries()

    expected_addl_at_max = {
        ConditionComposite(): 3.31 * 2,
        ConditionComposite([Condition.SELF_PASSIVE_ENHANCED]): 3.64 * 2,
    }

    expected = set(expected_addl_at_max.keys())
    actual = {entry.condition_comp for entry in possible_entries}

    assert actual == expected, actual.symmetric_difference(expected)

    for entry in possible_entries:
        assert \
            entry.total_mod_at_max == pytest.approx(expected_addl_at_max[entry.condition_comp]), \
            entry.condition_comp
        del expected_addl_at_max[entry.condition_comp]

    assert len(expected_addl_at_max) == 0, f"Conditions not tested: {set(expected_addl_at_max.keys())}"


def test_unique_dragon_ult(asset_manager: AssetManager, transformer_skill: SkillTransformer):
    # Lathna Unique Dragon Ult
    # https://dragalialost.wiki/w/Nyarlathotep_(Lathna)
    ability_ids = asset_manager.asset_chara_data.get_data_by_id(10550502).ability_ids_all_level
    skill_data_base = transformer_skill.transform_attacking(299000041, ability_ids=ability_ids)

    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        2.98 * 2,
        3.31 * 2,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3.31 * 2)
    assert skill_data.mods == approx_matrix([
        [2.98] * 2,
        [3.31] * 2,
    ])
    assert skill_data.mods_at_max == pytest.approx([3.31] * 2)
    assert skill_data.max_level == 2

    skill_data = skill_data_base.with_conditions(ConditionComposite(Condition.SELF_PASSIVE_ENHANCED))

    assert skill_data.hit_count == [2, 2]
    assert skill_data.hit_count_at_max == 2
    assert skill_data.total_mod == pytest.approx([
        3.28 * 2,
        3.64 * 2,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(3.64 * 2)
    assert skill_data.mods == approx_matrix([
        [3.28] * 2,
        [3.64] * 2,
    ])
    assert skill_data.mods_at_max == pytest.approx([3.64] * 2)
    assert skill_data.max_level == 2
