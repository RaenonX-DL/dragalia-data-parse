import pytest

from dlparse.transformer import SkillTransformer


def test_s2_0_stack_and_as_shared(transformer_skill: SkillTransformer):
    # Catherine S2
    # https://dragalialost.gamepedia.com/Catherine
    skill_data_base = transformer_skill.transform_attacking(105502042)

    # 0 Stack & SS
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [46, 46, 46]
    assert skill_data.hit_count_at_max == 46
    assert skill_data.total_mod == pytest.approx([0.44 * 46, 0.54 * 46, 0.54 * 46])
    assert skill_data.total_mod_at_max == pytest.approx(0.54 * 46)
    assert skill_data.mods == [[0.44] * 46, [0.54] * 46, [0.54] * 46]
    assert skill_data.mods_at_max == [0.54] * 46
    assert skill_data.max_level == 3


def test_s2_1_stack(transformer_skill: SkillTransformer):
    # Catherine S2
    # https://dragalialost.gamepedia.com/Catherine
    skill_data_base = transformer_skill.transform_attacking(105502043)

    # 1 Stack
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [58, 58, 58]
    assert skill_data.hit_count_at_max == 58
    assert skill_data.total_mod == pytest.approx([0.44 * 58, 0.54 * 58, 0.54 * 58])
    assert skill_data.total_mod_at_max == pytest.approx(0.54 * 58)
    assert skill_data.mods == [[0.44] * 58, [0.54] * 58, [0.54] * 58]
    assert skill_data.mods_at_max == [0.54] * 58
    assert skill_data.max_level == 3


def test_s2_2_stack(transformer_skill: SkillTransformer):
    # Catherine S2
    # https://dragalialost.gamepedia.com/Catherine
    skill_data_base = transformer_skill.transform_attacking(105502044)

    # 2 Stacks
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [66, 66, 66]
    assert skill_data.hit_count_at_max == 66
    assert skill_data.total_mod == pytest.approx([0.44 * 66, 0.54 * 66, 0.54 * 66])
    assert skill_data.total_mod_at_max == pytest.approx(0.54 * 66)
    assert skill_data.mods == [[0.44] * 66, [0.54] * 66, [0.54] * 66]
    assert skill_data.mods_at_max == [0.54] * 66
    assert skill_data.max_level == 3


def test_s2_3_stack(transformer_skill: SkillTransformer):
    # Catherine S2
    # https://dragalialost.gamepedia.com/Catherine
    skill_data_base = transformer_skill.transform_attacking(105502045)

    # 3 Stacks
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [74, 74, 74]
    assert skill_data.hit_count_at_max == 74
    assert skill_data.total_mod == pytest.approx([0.44 * 37 + 1.1 * 37, 0.54 * 37 + 1.22 * 37, 0.54 * 37 + 1.22 * 37])
    assert skill_data.total_mod_at_max == pytest.approx(0.54 * 37 + 1.22 * 37)
    assert skill_data.mods == [[0.44, 1.1] * 37, [0.54, 1.22] * 37, [0.54, 1.22] * 37]
    assert skill_data.mods_at_max == [0.54, 1.22] * 37
    assert skill_data.max_level == 3


def test_s2_as_helper(transformer_skill: SkillTransformer):
    # Catherine S2
    # https://dragalialost.gamepedia.com/Catherine
    skill_data_base = transformer_skill.transform_attacking(105502046)

    # As helper (unique)
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [46, 46, 46]
    assert skill_data.hit_count_at_max == 46
    assert skill_data.total_mod == pytest.approx([0.44 * 46, 0.54 * 46, 0.54 * 46])
    assert skill_data.total_mod_at_max == pytest.approx(0.54 * 46)
    assert skill_data.mods == [[0.44] * 46, [0.54] * 46, [0.54] * 46]
    assert skill_data.mods_at_max == [0.54] * 46
    assert skill_data.max_level == 3
