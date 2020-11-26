import pytest

from dlparse.transformer import SkillTransformer


def test_lapis_s2(transformer_skill: SkillTransformer):
    # Lapis S2
    pass


def test_elisanne_s1(transformer_skill: SkillTransformer):
    # Elisanne S1
    # https://dragalialost.gamepedia.com/Elisanne
    skill_data_base = transformer_skill.transform_attacking(105402011)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [0, 0, 0, 5]
    assert skill_data.hit_count_at_max == 5
    assert skill_data.total_mod == pytest.approx([0, 0, 0, 7.5])
    assert skill_data.total_mod_at_max == pytest.approx(7.5)
    assert skill_data.mods == [[], [], [], [1.5] * 5]
    assert skill_data.mods_at_max == [1.5] * 5
    assert skill_data.max_level == 4


def test_bellina_s1(transformer_skill: SkillTransformer):
    # Bellina S1
    # https://dragalialost.gamepedia.com/Bellina
    skill_data_base = transformer_skill.transform_attacking(103505033)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [5, 5, 5]
    assert skill_data.hit_count_at_max == 5
    assert skill_data.total_mod == pytest.approx([1.63 * 5, 1.81 * 5, 2.02 * 5])
    assert skill_data.total_mod_at_max == pytest.approx(2.02 * 5)
    assert skill_data.mods == [[1.63] * 5, [1.81] * 5, [2.02] * 5]
    assert skill_data.mods_at_max == [2.02] * 5
    assert skill_data.max_level == 3


def test_eugene_s1(transformer_skill: SkillTransformer):
    # Eugene S1
    # https://dragalialost.gamepedia.com/Eugene
    # One todo tag affiliated, check list after completion
    pass


def test_formal_joachim_s1_explosion(transformer_skill: SkillTransformer):
    # Formal Joachim S1 Explosion (S2-S1)
    # https://dragalialost.gamepedia.com/Formal_Joachim
    pass


def test_summer_mikoto_s1_celestial(transformer_skill: SkillTransformer):
    # Summer Mikoto S1 (Celestial)
    # https://dragalialost.gamepedia.com/Summer_Mikoto
    pass


def test_nevin_s2(transformer_skill: SkillTransformer):
    # Nevin S2
    # https://dragalialost.gamepedia.com/Nevin
    pass
    # skill_data_base = transformer_skill.transform_attacking(103505042)
    #
    # # Base data
    # skill_data = skill_data_base.with_conditions()
    #
    # # TODO: To be investigated
    # #   Seems that Sigil locked and Sigil released are using the same action file with different bullet? (10 / 10+1)
    #
    # assert skill_data.hit_count == [2, 2, 2, 2]
    # assert skill_data.hit_count_at_max == 2
    # assert skill_data.total_mod == pytest.approx([5.96 * 2, 6.63 * 2, 7.36 * 2, 8.18 * 2])
    # assert skill_data.total_mod_at_max == pytest.approx(16.36)
    # assert skill_data.mods == [[5.96] * 2, [6.63] * 2, [7.36] * 2, [8.18] * 2]
    # assert skill_data.mods_at_max == [8.18] * 2
    # assert skill_data.max_available_level == 4
