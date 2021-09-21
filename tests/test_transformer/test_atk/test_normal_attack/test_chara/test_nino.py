import pytest

from dlparse.transformer import AttackingActionTransformer


def test_dragondrive(transformer_atk: AttackingActionTransformer):
    # Nino (10150305)
    # - Mode 95: Unique Transform
    # - Unique Combo 67
    # - Action ID 101100
    data = transformer_atk.transform_normal_attack_or_fs(101100).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([0.15, 0.9])
    assert combo_1.sp_gain == 150
    assert combo_1.utp_gain == 45
    assert combo_1.od_rate == [1.0, 1.0]

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([0.15, 0.96])
    assert combo_2.sp_gain == 150
    assert combo_2.utp_gain == 45
    assert combo_2.od_rate == [1.0, 1.0]

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([0.15, 1.14])
    assert combo_3.sp_gain == 196
    assert combo_3.utp_gain == 85
    assert combo_3.od_rate == [1.0, 1.0]

    combo_4 = data[3]
    assert combo_4.mods == pytest.approx([0.15, 0.15, 1.2])
    assert combo_4.sp_gain == 265
    assert combo_4.utp_gain == 180
    assert combo_4.od_rate == [1.0, 1.0, 1.0]

    combo_5 = data[4]
    assert combo_5.mods == pytest.approx([0.15, 0.15, 0.15, 1.8])
    assert combo_5.sp_gain == 391
    assert combo_5.utp_gain == 250
    assert combo_5.od_rate == [1.0, 1.0, 1.0, 1.0]
