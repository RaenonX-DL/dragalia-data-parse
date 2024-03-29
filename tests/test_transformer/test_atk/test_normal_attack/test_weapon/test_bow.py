import pytest

from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Bow Lv. 1 (600000)
    data = transformer_atk.transform_normal_attack_or_fs(600000).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == pytest.approx([0.35] * 3)
    assert combo_1.sp_gain == 184
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 3

    combo_2 = data[1]
    assert combo_2.mods == pytest.approx([0.44] * 2)
    assert combo_2.sp_gain == 92
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 2

    combo_3 = data[2]
    assert combo_3.mods == pytest.approx([0.50] * 3)
    assert combo_3.sp_gain == 276
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 3

    combo_4 = data[3]
    assert combo_4.mods == pytest.approx([0.76] * 2)
    assert combo_4.sp_gain == 414
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0] * 2

    combo_5 = data[4]
    assert combo_5.mods == pytest.approx([0.42] * 5)
    assert combo_5.sp_gain == 529
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0] * 5


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Bow Lv. 2 (600000)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(600000, 2).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == pytest.approx([0.44] * 3)
    assert combo_1.sp_gain == 184
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0] * 3

    combo_2 = normal_attack_data[1]
    assert combo_2.mods == pytest.approx([0.55] * 2)
    assert combo_2.sp_gain == 92
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0] * 2

    combo_3 = normal_attack_data[2]
    assert combo_3.mods == pytest.approx([0.63] * 3)
    assert combo_3.sp_gain == 276
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 3

    combo_4 = normal_attack_data[3]
    assert combo_4.mods == pytest.approx([0.95] * 2)
    assert combo_4.sp_gain == 414
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0] * 2

    combo_5 = normal_attack_data[4]
    assert combo_5.mods == pytest.approx([0.53] * 5)
    assert combo_5.sp_gain == 529
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0] * 5
