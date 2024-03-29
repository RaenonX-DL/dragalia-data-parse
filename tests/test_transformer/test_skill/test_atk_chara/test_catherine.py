import pytest

from dlparse.enums import ConditionComposite
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_iter_entries(transformer_skill: SkillTransformer):
    skill_id_mods = {
        105502042: 0.60 * 46,
        105502043: 0.60 * 58,
        105502044: 0.60 * 66,
        105502045: 0.60 * 37 + 1.30 * 37,
        105502046: 0.60 * 46
    }

    for skill_id, total_mod in skill_id_mods.items():
        skill_data = transformer_skill.transform_attacking(skill_id)

        possible_entries = skill_data.get_all_possible_entries()

        expected_max_total_mods = {
            ConditionComposite(): total_mod,
        }

        expected = set(expected_max_total_mods.keys())
        actual = {entry.condition_comp for entry in possible_entries}

        assert expected == actual, actual.symmetric_difference(expected)

        for entry in possible_entries:
            assert entry.total_mod_at_max == pytest.approx(expected_max_total_mods[entry.condition_comp])
            del expected_max_total_mods[entry.condition_comp]

        assert len(expected_max_total_mods) == 0, f"Conditions not tested: {set(expected_max_total_mods.keys())}"


def test_s2_0_stack_and_as_shared(transformer_skill: SkillTransformer):
    # Catherine S2
    # https://dragalialost.wiki/w/Catherine
    skill_data_base = transformer_skill.transform_attacking(105502042)

    # 0 Stack & SS
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [46, 46, 46, 46]
    assert skill_data.hit_count_at_max == 46
    assert skill_data.total_mod == pytest.approx([0.44 * 46, 0.54 * 46, 0.6 * 46, 0.6 * 46])
    assert skill_data.total_mod_at_max == pytest.approx(0.6 * 46)
    assert skill_data.mods == approx_matrix([[0.44] * 46, [0.54] * 46, [0.6] * 46, [0.6] * 46])
    assert skill_data.mods_at_max == pytest.approx([0.6] * 46)
    assert skill_data.max_level == 4


def test_s2_1_stack(transformer_skill: SkillTransformer):
    # Catherine S2
    # https://dragalialost.wiki/w/Catherine
    skill_data_base = transformer_skill.transform_attacking(105502043)

    # 1 Stack
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [58, 58, 58, 58]
    assert skill_data.hit_count_at_max == 58
    assert skill_data.total_mod == pytest.approx([0.44 * 58, 0.54 * 58, 0.6 * 58, 0.6 * 58])
    assert skill_data.total_mod_at_max == pytest.approx(0.6 * 58)
    assert skill_data.mods == approx_matrix([[0.44] * 58, [0.54] * 58, [0.6] * 58, [0.6] * 58])
    assert skill_data.mods_at_max == pytest.approx([0.6] * 58)
    assert skill_data.max_level == 4


def test_s2_2_stack(transformer_skill: SkillTransformer):
    # Catherine S2
    # https://dragalialost.wiki/w/Catherine
    skill_data_base = transformer_skill.transform_attacking(105502044)

    # 2 Stacks
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [66, 66, 66, 66]
    assert skill_data.hit_count_at_max == 66
    assert skill_data.total_mod == pytest.approx([0.44 * 66, 0.54 * 66, 0.6 * 66, 0.6 * 66])
    assert skill_data.total_mod_at_max == pytest.approx(0.6 * 66)
    assert skill_data.mods == approx_matrix([[0.44] * 66, [0.54] * 66, [0.6] * 66, [0.6] * 66])
    assert skill_data.mods_at_max == pytest.approx([0.6] * 66)
    assert skill_data.max_level == 4


def test_s2_3_stack(transformer_skill: SkillTransformer):
    # Catherine S2
    # https://dragalialost.wiki/w/Catherine
    skill_data_base = transformer_skill.transform_attacking(105502045)

    # 3 Stacks
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [74, 74, 74, 74]
    assert skill_data.hit_count_at_max == 74
    assert skill_data.total_mod == pytest.approx([
        0.44 * 37 + 1.1 * 37,
        0.54 * 37 + 1.22 * 37,
        0.6 * 37 + 1.3 * 37,
        0.6 * 37 + 1.3 * 37,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(0.6 * 37 + 1.3 * 37)
    assert skill_data.mods == approx_matrix([[0.44, 1.1] * 37, [0.54, 1.22] * 37, [0.6, 1.3] * 37, [0.6, 1.3] * 37])
    assert skill_data.mods_at_max == pytest.approx([0.6, 1.3] * 37)
    assert skill_data.max_level == 4


def test_s2_as_helper(transformer_skill: SkillTransformer):
    # Catherine S2
    # https://dragalialost.wiki/w/Catherine
    skill_data_base = transformer_skill.transform_attacking(105502046)

    # As helper (unique)
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [46, 46, 46, 46]
    assert skill_data.hit_count_at_max == 46
    assert skill_data.total_mod == pytest.approx([0.44 * 46, 0.54 * 46, 0.6 * 46, 0.6 * 46])
    assert skill_data.total_mod_at_max == pytest.approx(0.6 * 46)
    assert skill_data.mods == approx_matrix([[0.44] * 46, [0.54] * 46, [0.6] * 46, [0.6] * 46])
    assert skill_data.mods_at_max == pytest.approx([0.6] * 46)
    assert skill_data.max_level == 4
