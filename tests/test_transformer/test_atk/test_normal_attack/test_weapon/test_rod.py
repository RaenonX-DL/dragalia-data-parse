import pytest

from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Wand Lv. 1 (700000)
    data = transformer_atk.transform_normal_attack_or_fs(700000).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([1.18])
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([0.64] * 2)
    assert combo_2.sp_gain == 200
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 2

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([0.43] * 3)
    assert combo_3.sp_gain == 240
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 3

    combo_4 = data[3]
    assert combo_4.mods == pytest.approx([0.94] * 2)
    assert combo_4.sp_gain == 430
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0] * 2

    combo_5 = data[4]
    assert combo_5.mods == pytest.approx([0.74] + [0.43] * 4)
    assert combo_5.sp_gain == 600
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0] * 5


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Wand Lv. 2 (700000)
    data = transformer_atk.transform_normal_attack_or_fs(700000, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([1.36])
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([0.74] * 2)
    assert combo_2.sp_gain == 200
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 2

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([0.49] * 3)
    assert combo_3.sp_gain == 240
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 3

    combo_4 = data[3]
    assert combo_4.mods == pytest.approx([1.08] * 2)
    assert combo_4.sp_gain == 430
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0] * 2

    combo_5 = data[4]
    assert combo_5.mods == pytest.approx([0.85] + [0.49] * 4)
    assert combo_5.sp_gain == 600
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0] * 5
