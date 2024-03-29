import pytest

from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Blade Lv. 1 (200000)
    data = transformer_atk.transform_normal_attack_or_fs(200000).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([1.16])
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([1.164])
    assert combo_2.sp_gain == 130
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([0.76] * 2)
    assert combo_3.sp_gain == 220
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 2

    combo_4 = data[3]
    assert combo_4.mods == pytest.approx([1.55])
    assert combo_4.sp_gain == 360
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = data[4]
    assert combo_5.mods == pytest.approx([1.72] * 2)
    assert combo_5.sp_gain == 900
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0] * 2


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Blade Lv. 2 (200000)
    data = transformer_atk.transform_normal_attack_or_fs(200000, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([1.28])
    assert combo_1.sp_gain == 130
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([1.28])
    assert combo_2.sp_gain == 130
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([0.84] * 2)
    assert combo_3.sp_gain == 220
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 2

    combo_4 = data[3]
    assert combo_4.mods == pytest.approx([1.71])
    assert combo_4.sp_gain == 360
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = data[4]
    assert combo_5.mods == pytest.approx([1.89] * 2)
    assert combo_5.sp_gain == 900
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0] * 2
