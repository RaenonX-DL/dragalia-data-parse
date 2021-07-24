from dlparse.transformer import AttackingActionTransformer


def test_default_normal_attack(transformer_atk: AttackingActionTransformer):
    # Lance Lv. 1 (500000)
    data = transformer_atk.transform_normal_attack_or_fs(500000).with_condition()

    combo_1 = data[0]
    assert combo_1.mods == [1.01]
    assert combo_1.sp_gain == 120
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = data[1]
    assert combo_2.mods == [0.54, 0.54]
    assert combo_2.sp_gain == 240
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0, 1.0]

    combo_3 = data[2]
    assert combo_3.mods == [1.30]
    assert combo_3.sp_gain == 120
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0]

    combo_4 = data[3]
    assert combo_4.mods == [1.80]
    assert combo_4.sp_gain == 480
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = data[4]
    assert combo_5.mods == [1.34]
    assert combo_5.sp_gain == 600
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0]


def test_default_normal_attack_lv2(transformer_atk: AttackingActionTransformer):
    # Lance Lv. 2 (500000)
    normal_attack_data = transformer_atk.transform_normal_attack_or_fs(500000, 2).with_condition()

    combo_1 = normal_attack_data[0]
    assert combo_1.mods == [1.11]
    assert combo_1.sp_gain == 120
    assert combo_1.utp_gain == 0
    assert combo_1.od_rate == [1.0]

    combo_2 = normal_attack_data[1]
    assert combo_2.mods == [0.59, 0.59]
    assert combo_2.sp_gain == 240
    assert combo_2.utp_gain == 0
    assert combo_2.od_rate == [1.0, 1.0]

    combo_3 = normal_attack_data[2]
    assert combo_3.mods == [1.43]
    assert combo_3.sp_gain == 120
    assert combo_3.utp_gain == 0
    assert combo_3.od_rate == [1.0]

    combo_4 = normal_attack_data[3]
    assert combo_4.mods == [1.98]
    assert combo_4.sp_gain == 480
    assert combo_4.utp_gain == 0
    assert combo_4.od_rate == [1.0]

    combo_5 = normal_attack_data[4]
    assert combo_5.mods == [1.47]
    assert combo_5.sp_gain == 600
    assert combo_5.utp_gain == 0
    assert combo_5.od_rate == [1.0]
