import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1(transformer_skill: SkillTransformer):
    # Gala Laxi S1
    # https://dragalialost.gamepedia.com/Gala_Laxi
    skill_data_base = transformer_skill.transform_attacking(103501021)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        1.686 * 4,
        1.897 * 4,
        2.108 * 4
    ])
    assert skill_data.total_mod_at_max == pytest.approx(2.108 * 4)
    assert skill_data.mods == approx_matrix([
        [1.686] * 4,
        [1.897] * 4,
        [2.108] * 4
    ])
    assert skill_data.mods_at_max == pytest.approx([2.108] * 4)
    assert skill_data.max_level == 3


def test_s1_eden(transformer_skill: SkillTransformer):
    # Gala Laxi S1 @ Eden
    # https://dragalialost.gamepedia.com/Gala_Laxi
    skill_data_base = transformer_skill.transform_attacking(103501023)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [12, 12, 12]
    assert skill_data.hit_count_at_max == 12
    assert skill_data.total_mod == pytest.approx([
        0.595 * 2 + 0.793 * 4 + 0.992 * 6,
        0.669 * 2 + 0.892 * 4 + 1.116 * 6,
        0.744 * 2 + 0.992 * 4 + 1.24 * 6,
    ])
    assert skill_data.total_mod_at_max == pytest.approx(0.744 * 2 + 0.992 * 4 + 1.24 * 6)
    assert skill_data.mods == approx_matrix([
        [0.595, 0.992] * 2 + [0.793, 0.992] * 2 + [0.992, 0.793] * 2,
        [0.669, 1.116] * 2 + [0.892, 1.116] * 2 + [1.116, 0.892] * 2,
        [0.744, 1.24] * 2 + [0.992, 1.24] * 2 + [1.24, 0.992] * 2,
    ])
    assert skill_data.mods_at_max == pytest.approx([0.744, 1.24] * 2 + [0.992, 1.24] * 2 + [1.24, 0.992] * 2)
    assert skill_data.max_level == 3


def test_s2_eden(transformer_skill: SkillTransformer):
    # Gala Laxi S2 @ Eden
    # https://dragalialost.gamepedia.com/Gala_Laxi
    skill_data_base = transformer_skill.transform_attacking(103501024)

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [4, 4]
    assert skill_data.hit_count_at_max == 4
    assert skill_data.total_mod == pytest.approx([
        4.48 * 3 + 4.928,
        5.6 * 3 + 6.16
    ])
    assert skill_data.total_mod_at_max == pytest.approx(5.6 * 3 + 6.16)
    assert skill_data.mods == approx_matrix([
        [4.48] * 3 + [4.928],
        [5.6] * 3 + [6.16]
    ])
    assert skill_data.mods_at_max == pytest.approx([5.6] * 3 + [6.16])
    assert skill_data.max_level == 2


def test_s2_call_fig(transformer_skill: SkillTransformer):
    # Gala Laxi Fig
    # https://dragalialost.gamepedia.com/Gala_Laxi
    skill_data_base = transformer_skill.transform_attacking(103501022)

    # TEST: TBA - GaLaxi S2 (Fig)
    # AID 391270 (Main action) auto fires 391272 (Fig bullets)
    #   SID - 103501022
    #   Find how did the action canceled
    #   _autoFireInterval / _autoFireActionId

    # Base data
    # skill_data = skill_data_base.with_conditions()
    #
    # assert skill_data.hit_count == [59, 59]
    # assert skill_data.hit_count_at_max == 59
    # assert skill_data.total_mod == pytest.approx([
    #     0.333 * 59,
    #     1 * 59
    # ])
    # assert skill_data.total_mod_at_max == pytest.approx(59)
    # assert skill_data.mods == approx_matrix([
    #     [0.333] * 59,
    #     [1] * 59
    # ])
    # assert skill_data.mods_at_max == pytest.approx([1] * 59)
    # assert skill_data.max_level == 2
