from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Staff Lv. 1 (800000)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(800000).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == [1.14]
    assert combo_1.sp_gain == 232
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data[1]
    assert combo_2.mods == [1.32]
    assert combo_2.sp_gain == 232
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = normal_attack_data[2]
    assert combo_3.mods == [0.74] * 2
    assert combo_3.sp_gain == 348
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 2

    combo_4 = normal_attack_data[3]
    assert combo_4.mods == [2.48]
    assert combo_4.sp_gain == 464
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = normal_attack_data[4]
    assert combo_5.mods == [3.23]
    assert combo_5.sp_gain == 696
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0]


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Staff Lv. 2 (800000)
    data = transformer_atk.transform_normal_attack_or_fs(800000, 2).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [1.24]
    assert combo_1.sp_gain == 232
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == [1.44]
    assert combo_2.sp_gain == 232
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0]

    combo_3 = data[2]
    assert combo_3.mods == [0.81] * 2
    assert combo_3.sp_gain == 348
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0] * 2

    combo_4 = data[3]
    assert combo_4.mods == [2.70]
    assert combo_4.sp_gain == 464
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = data[4]
    assert combo_5.mods == [3.53]
    assert combo_5.sp_gain == 696
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0]
