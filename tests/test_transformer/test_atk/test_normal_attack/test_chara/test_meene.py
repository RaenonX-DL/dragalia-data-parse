import pytest

from dlparse.transformer import AttackingActionTransformer


def test_normal(transformer_atk: AttackingActionTransformer):
    # Meene (10650303)
    # - Mode 56: Normal
    # - Unique Combo 43
    # - Action ID 601700
    data = transformer_atk.transform_normal_attack_or_fs(601700).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([0.43] * 7)
    assert combo_1.sp_gain == 350
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 7

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([0.43] * 14)
    assert combo_2.sp_gain == 400
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 14

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([0.43] * 21)
    assert combo_3.sp_gain == 450
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 21
