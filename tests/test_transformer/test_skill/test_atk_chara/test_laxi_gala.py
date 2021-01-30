import pytest

from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1(transformer_skill: SkillTransformer):
    # Gala Laxi S1
    # https://dragalialost.wiki/w/Gala_Laxi
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
    # https://dragalialost.wiki/w/Gala_Laxi
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
    # https://dragalialost.wiki/w/Gala_Laxi
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


def test_s2_call_fig():
    # Gala Laxi Fig
    # https://dragalialost.wiki/w/Gala_Laxi
    # skill_data_base = transformer_skill.transform_attacking(103501022)

    pass

    # TEST: TBA - GaLaxi S2 (Fig)
    #   SID 103501022
    #   AID 391270
    #   - DAG_127_04_H01_LV01
    #   - ActionPartsStockBullet Fires 391272
    #   -------------------
    #   DAG_127_04_H01_LV01
    #   - (Dead end)
    #   -------------------
    #   CID 10350102
    #   - ABID 2 - 1064
    #   -------------------
    #   - ABID 1064
    #     - Ref ABID 1068?
    #     - Ref ABID 1094
    #     - Ref ABID 1099?
    #   -------------------
    #   - ABID 1094
    #     - Cond 64 - Req 994, -1 / 0
    #       - REQUIRED_BUFF_AND_SP1_MORE
    #     - Type 61, IDA: 1
    #       - Change to Mode 1
    #     - Ref ABID 1095
    #   - ABID 1095
    #     - Cond 70 - 994 / 0
    #       - BUFF_DISAPPEARED When ACID 994 disappear?
    #     - Type 61, IDA: 0
    #       - Change to Mode 0
    #     - Type 60
    #       - Remove Stock Bullets
    #     - Ref ABID 1116
    #   - ABID 1116
    #     - Cond 70 - 994 / 0
    #       - BUFF_DISAPPEARED When ACID 994 disappear?
    #     - Type 14 - ACID 1075
    #     - Type 14 - ACID 1077
    #     - Type 14 - ACID 1079

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
